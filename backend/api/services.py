from recipe_scrapers import scrape_html
import requests
from fractions import Fraction
import re
import logging
from decimal import Decimal
from typing import Dict, List, Tuple
from .models import Recipe, Ingredient, RecipeIngredient
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

UNIT_MAPPING = {
    'cup': 'cup',
    'cups': 'cup',
    'tablespoon': 'tbsp',
    'tablespoons': 'tbsp',
    'tbsp': 'tbsp',
    'teaspoon': 'tsp',
    'teaspoons': 'tsp',
    'tsp': 'tsp',
    'ounce': 'oz',
    'ounces': 'oz',
    'oz': 'oz',
    'pound': 'lb',
    'pounds': 'lb',
    'lb': 'lb',
    'gram': 'g',
    'grams': 'g',
    'g': 'g',
    'kilogram': 'kg',
    'kilograms': 'kg',
    'kg': 'kg',
    'milliliter': 'ml',
    'milliliters': 'ml',
    'ml': 'ml',
    'liter': 'l',
    'liters': 'l',
    'l': 'l',
    'pinch': 'pinch',
    'piece': 'piece',
    'pieces': 'piece',
    'slice': 'slice',
    'slices': 'slice',
    'whole': 'whole',
    'package': 'pkg', 'packages': 'pkg', 'pkg': 'pkg',
}

def extract_quantity_and_unit(text):
    """Extract quantity and unit from ingredient text."""
    # Common fraction patterns
    fraction_pattern = r'(\d+(?:/\d+)?|\d+\s+\d+/\d+)'
    # Unit pattern based on UNIT_MAPPING
    unit_pattern = '|'.join(UNIT_MAPPING.keys())
    
    # Match patterns like "2", "1/2", "2 1/2" followed by optional unit
    pattern = rf'^({fraction_pattern})\s*({unit_pattern})?\s+(.+)$'
    match = re.match(pattern, text, re.IGNORECASE)
    
    if not match:
        # If no match, try to find just a number at the start
        number_match = re.match(r'^(\d+)\s+(.+)$', text)
        if number_match:
            return float(number_match.group(1)), 'piece', number_match.group(2)
        return 1, 'whole', text

    quantity_str, unit, ingredient = match.groups()
    
    # Convert fraction to decimal
    if '/' in quantity_str:
        if ' ' in quantity_str:
            whole, frac = quantity_str.split()
            num, denom = map(int, frac.split('/'))
            quantity = float(whole) + num/denom
        else:
            num, denom = map(int, quantity_str.split('/'))
            quantity = num/denom
    else:
        quantity = float(quantity_str)

    # Map unit to standard form
    if unit:
        unit = UNIT_MAPPING.get(unit.lower(), 'piece')
    else:
        unit = 'piece'

    return quantity, unit, ingredient.strip()

def parse_ingredient_line(line: str) -> Tuple[str, float, str, str]:
    """Parse an ingredient line into (ingredient_name, quantity, unit, notes)"""
    # Extract notes in parentheses
    notes = []
    for note in re.finditer(r'\(([^)]+)\)', line):
        notes.append(note.group(1))
    if notes:
        notes = ', '.join(notes)
        line = re.sub(r'\([^)]*\)', '', line).strip()
    else:
        notes = ''

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
        'package': 'pkg', 'packages': 'pkg', 'pkg': 'pkg',
        'whole': 'whole',
        'large': 'whole',
        'medium': 'whole',
        'small': 'whole'
    }
    
    # Try to find quantity and unit
    words = line.lower().split()
    if not words:
        return '', 1.0, 'whole', notes
        
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
                if ' ' in first_num:
                    whole, frac = first_num.split()
                    num, denom = map(int, frac.split('/'))
                    quantity = float(whole) + num/denom
                else:
                    num, denom = map(int, first_num.split('/'))
                    quantity = num/denom
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
                num, denom = map(int, words[i + 1].split('/'))
                quantity = whole + num/denom
                ingredient_start = i + 2
                break
            elif '/' in word:
                # Handle fractions like "1/2"
                num, denom = map(int, word.split('/'))
                quantity = num/denom
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

def scrape_recipe(url: str, user=None) -> Dict:
    """Scrape recipe data from a URL."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract recipe name from title
        title = soup.find('title')
        name = title.text.strip() if title else 'Untitled Recipe'
        if '|' in name:
            name = name.split('|')[0].strip()
        
        # Find ingredient list (this is a simplified example)
        ingredient_list = []
        ingredients_div = soup.find(class_='recipe-ingredients')
        if ingredients_div:
            for item in ingredients_div.find_all('li'):
                try:
                    ingredient_data = process_ingredient_line(item.text.strip())
                    ingredient_list.append(ingredient_data)
                except Exception as e:
                    logger.error(f'Error processing ingredient: {e}')
                    continue
        
        # Find instructions
        instructions = ''
        instructions_div = soup.find(class_='recipe-instructions')
        if instructions_div:
            instructions = '\n'.join(
                f'{i+1}. {step.text.strip()}'
                for i, step in enumerate(instructions_div.find_all('li'))
            )
        
        recipe_data = {
            'name': name,
            'instructions': instructions,
            'ingredients': ingredient_list
        }
        if user:
            recipe_data['user'] = user.id
            
        return recipe_data
        
    except Exception as e:
        logger.error(f'Error scraping recipe from {url}: {e}')
        raise

def parse_servings(servings_str: str) -> int:
    """Parse servings string to get the number"""
    if not servings_str:
        return 4  # default servings
    
    # Try to extract the first number from the string
    match = re.search(r'\d+', servings_str)
    if match:
        return int(match.group())
    return 4

def process_ingredient_line(line):
    """Process a single ingredient line into structured data."""
    try:
        # Parse the ingredient line
        ingredient_name, quantity, unit, notes = parse_ingredient_line(line)
        
        # Guess ingredient category
        category = 'other'
        if any(word in ingredient_name.lower() for word in ['flour', 'sugar', 'oil', 'vinegar', 'sauce']):
            category = 'pantry'
        elif any(word in ingredient_name.lower() for word in ['salt', 'pepper', 'spice', 'herb']):
            category = 'spices'
        elif any(word in ingredient_name.lower() for word in ['milk', 'cream', 'cheese', 'butter', 'egg']):
            category = 'dairy'
        elif any(word in ingredient_name.lower() for word in ['beef', 'chicken', 'pork', 'fish']):
            category = 'meat'
        elif any(word in ingredient_name.lower() for word in ['apple', 'banana', 'carrot', 'onion', 'garlic']):
            category = 'produce'

        return {
            'ingredient': {
                'name': ingredient_name,
                'category': category
            },
            'quantity': quantity,
            'unit': unit,
            'notes': notes
        }
    except Exception as e:
        logger.error(f'Error processing ingredient line {line!r}: {e}')
        raise
