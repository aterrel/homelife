from recipe_scrapers import scrape_html
import requests
from fractions import Fraction
import re
import logging
from decimal import Decimal
from typing import Dict, List, Tuple
from .models import Recipe, Ingredient, RecipeIngredient

logger = logging.getLogger(__name__)

def parse_servings(servings_str: str) -> int:
    """Parse servings string to get the number"""
    if not servings_str:
        return 4  # default servings
    
    # Try to extract the first number from the string
    match = re.search(r'\d+', servings_str)
    if match:
        return int(match.group())
    return 4

def parse_ingredient_line(line: str) -> Tuple[str, float, str, str]:
    """Parse an ingredient line into (ingredient_name, quantity, unit, notes)"""
    logger.debug(f"Parsing ingredient line: {line}")
    
    # Remove leading/trailing whitespace and bullet points
    line = line.strip().lstrip('*-•').strip()
    
    # Extract notes (anything in parentheses)
    notes = ''
    if '(' in line:
        notes = re.findall(r'\((.*?)\)', line)
        notes = ', '.join(notes)
        line = re.sub(r'\([^)]*\)', '', line).strip()

    # Common units to look for
    units = {
        'cups': 'cup', 'cup': 'cup',
        'tablespoons': 'tbsp', 'tablespoon': 'tbsp', 'tbsp': 'tbsp', 'tbsps': 'tbsp',
        'teaspoons': 'tsp', 'teaspoon': 'tsp', 'tsp': 'tsp', 'tsps': 'tsp',
        'ounces': 'oz', 'ounce': 'oz', 'oz': 'oz',
        'pounds': 'lb', 'pound': 'lb', 'lb': 'lb',
        'grams': 'g', 'gram': 'g', 'g': 'g',
        'kilograms': 'kg', 'kilogram': 'kg', 'kg': 'kg',
        'milliliters': 'ml', 'milliliter': 'ml', 'ml': 'ml',
        'liters': 'l', 'liter': 'l', 'l': 'l',
        'pieces': 'piece', 'piece': 'piece',
        'pinch': 'pinch', 'pinches': 'pinch',
        'package': 'package', 'packages': 'package', 'pkg': 'package',
    }
    
    # Try to find quantity and unit
    words = line.lower().split()
    if not words:
        return '', 1.0, 'whole', ''
        
    quantity = 1.0
    unit = 'whole'
    ingredient_start = 0
    
    # Handle ranges like "1/2 - 1 Tbsp"
    range_match = re.match(r'([\d\s/]+)\s*-\s*([\d\s/]+)\s*(\w+)(.*)', line.lower())
    if range_match:
        try:
            # Take the first number from the range
            first_num = range_match.group(1).strip()
            if '/' in first_num:
                quantity = float(sum(Fraction(s) for s in first_num.split()))
            else:
                quantity = float(first_num)
            unit_word = range_match.group(3).strip()
            if unit_word in units:
                unit = units[unit_word]
            ingredient_name = range_match.group(4).strip()
            return ingredient_name, quantity, unit, notes
        except ValueError:
            pass
    
    # Look for numeric values at the start
    for i, word in enumerate(words):
        try:
            if i + 2 < len(words) and '/' in words[i + 1]:
                # Handle mixed numbers like "1 1/2"
                whole = float(word)
                frac = float(sum(Fraction(s) for s in words[i + 1].split()))
                quantity = whole + frac
                ingredient_start = i + 2
                break
            elif '/' in word:
                # Handle fractions like "1/2"
                quantity = float(sum(Fraction(s) for s in word.split()))
                ingredient_start = i + 1
                break
            elif word.replace('.', '').isdigit():
                # Handle simple numbers
                quantity = float(word)
                ingredient_start = i + 1
                break
        except ValueError:
            break
            
    # Look for unit after the number
    if ingredient_start < len(words):
        next_word = words[ingredient_start]
        if next_word in units:
            unit = units[next_word]
            ingredient_start += 1
            
    # The rest is the ingredient name
    ingredient_name = ' '.join(words[ingredient_start:]).strip()
    
    logger.debug(f"Parsed ingredient: name='{ingredient_name}', quantity={quantity}, unit='{unit}', notes='{notes}'")
    return ingredient_name, quantity, unit, notes

def get_or_create_ingredient(name: str, category: str = 'other') -> Ingredient:
    """Get an existing ingredient or create a new one"""
    name = name.lower().strip()
    try:
        return Ingredient.objects.get(name=name)
    except Ingredient.DoesNotExist:
        logger.debug(f"Creating new ingredient: {name}")
        return Ingredient.objects.create(
            name=name,
            category=category
        )

def scrape_recipe(url: str, user) -> Recipe:
    """Scrape a recipe from a URL and create a Recipe object"""
    logger.info(f"Scraping recipe from URL: {url}")
    try:
        # Fetch the HTML content
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        logger.debug(f"Successfully fetched HTML content (length: {len(html)})")
        
        # Parse the recipe
        recipe_scraper = scrape_html(html, url)
        logger.debug("Successfully created recipe scraper")
        
        # Extract basic information
        title = recipe_scraper.title()
        description = recipe_scraper.description() if hasattr(recipe_scraper, 'description') else ''
        instructions = recipe_scraper.instructions_list()
        ingredients_list = recipe_scraper.ingredients()
        yields = recipe_scraper.yields()
        
        logger.debug(f"Extracted recipe info: title='{title}', instructions_count={len(instructions)}, ingredients_count={len(ingredients_list)}, yields='{yields}'")
        
        # Create the recipe
        recipe = Recipe.objects.create(
            name=title,
            description=description,
            instructions='\n'.join(instructions),
            prep_time=recipe_scraper.prep_time() if hasattr(recipe_scraper, 'prep_time') else 0,
            cook_time=recipe_scraper.cook_time() if hasattr(recipe_scraper, 'cook_time') else 0,
            servings=parse_servings(yields),
            difficulty='medium',  # Default value as most sites don't provide this
            user=user
        )
        logger.debug(f"Created recipe object with ID: {recipe.id}")
        
        # Process ingredients
        for ingredient_line in ingredients_list:
            try:
                name, quantity, unit, notes = parse_ingredient_line(ingredient_line)
                if not name:
                    logger.warning(f"Skipping empty ingredient line: {ingredient_line}")
                    continue
                    
                ingredient = get_or_create_ingredient(name)
                
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=Decimal(str(quantity)),  # Convert float to Decimal
                    unit=unit,
                    notes=notes
                )
                logger.debug(f"Added ingredient to recipe: {ingredient.name}")
            except Exception as e:
                logger.error(f"Error processing ingredient line '{ingredient_line}': {str(e)}")
                continue
        
        logger.info(f"Successfully scraped and created recipe: {title}")
        return recipe
        
    except Exception as e:
        logger.error(f"Error scraping recipe from {url}: {str(e)}")
        raise
