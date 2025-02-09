import datetime
import requests
from recipe_scrapers import scrape_html

import django
import os
import sys
import re
import time

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.append(project_root)
# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Recipe, Ingredient, RecipeIngredient, Category

UNIT_CHOICES = [
    'cup', 'tbsp', 'tsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l', 'pinch', 'piece', 'whole', 'pkg', 'slice'
]

# Helper function to parse quantity and units
def parse_quantity_and_units(ingredient_text):
    pattern = r'(\d+\/?\d*)?\s*(%s)?' % '|'.join(UNIT_CHOICES)
    match = re.match(pattern, ingredient_text, re.IGNORECASE)
    if match:
        quantity = match.group(1) if match.group(1) else 1
        units = match.group(2) if match.group(2) else 'piece'
        return quantity, units
    return 1, 'piece'

def parse_duration(minutes):
    duration = datetime.timedelta(minutes=minutes)
    return duration

# Function to parse recipe and return data as dictionary
def scrape_recipe_data(url):
    response = requests.get(url)
    html = response.text
    scraper = scrape_html(html, org_url=url)

    # Extract recipe details
    name = scraper.title()
    soup = scraper.soup

    prep_time = parse_duration(scraper.prep_time())
    cook_time = parse_duration(scraper.cook_time())
    servings_text = scraper.yields()
    match = re.match(r'(\d+) serving', servings_text)
    if match:
        servings = int(match.group(1))
    else:
        servings = -1
    instructions = scraper.instructions()

    # Extract ingredients
    ingredients = []
    ingredients_list = soup.find_all('span', class_='ingredients-item-name')
    for order, ingredient_text in enumerate(ingredients_list, start=1):
        full_ingredient_text = ingredient_text.get_text(strip=True)
        quantity, units = parse_quantity_and_units(full_ingredient_text)

        ingredient_name = re.sub(r'^\d+\/?\d*\s*(%s)?\s*' % '|'.join(UNIT_CHOICES), '', full_ingredient_text, flags=re.IGNORECASE).strip()
        
        ingredients.append({
            'name': ingredient_name,
            'quantity': quantity,
            'units': units,
            'order': order
        })

    return {
        'name': name,
        'prep_time': prep_time,
        'cook_time': cook_time,
        'servings': servings,
        'instructions': instructions,
        'url': url,
        'ingredients': ingredients
    }

# Function to create recipe and related objects in the database
def create_recipe_in_db(recipe_data):
    # Check if recipe already exists
    if Recipe.objects.filter(name=recipe_data['name']).exists():
        print(f'Recipe "{recipe_data["name"]}" already exists in the database.')
        return

    recipe = Recipe.objects.create(
        name=recipe_data['name'],
        prep_time=recipe_data['prep_time'],
        cook_time=recipe_data['cook_time'],
        servings=recipe_data['servings'],
        instructions=recipe_data['instructions'],
        url=recipe_data['url']
    )

    for ingredient_data in recipe_data['ingredients']:
        ingredient, created = Ingredient.objects.get_or_create(name=ingredient_data['name'])
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity=ingredient_data['quantity'],
            units=ingredient_data['units'],
            order=ingredient_data['order']
        )

    print(f'Recipe "{recipe_data["name"]}" added successfully.')


import requests
from bs4 import BeautifulSoup


# Function to get a list of recipe URLs from AllRecipes
def get_recipe_urls(base_url, num_recipes=5):
    recipe_urls = []
    page = 1

    page = 1
    while True:
        response = requests.get(f"{base_url}?page={page}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if not href.startswith('https://www.allrecipes.com/'):
                continue
            match = re.match(r'.*recipe-(\d{7})$', href)
            if match and href not in recipe_urls:
                yield href
                recipe_urls.append(href)
                if len(recipe_urls) == num_recipes:
                    return

        page += 1
        time.sleep(30)

    return recipe_urls

# Example usage
start_url = 'https://www.allrecipes.com/recipes/16492/everyday-cooking/special-collections/allrecipes-allstars/'

recipe_urls = [
    'https://www.allrecipes.com/passion-fruit-fizz-martini-recipe-8786408',
    'https://www.allrecipes.com/smoked-bologna-recipe-8786384',
    'https://www.allrecipes.com/meatball-subs-on-a-stick-recipe-8780157',
    'https://www.allrecipes.com/sticky-toffee-pudding-thumbprints-recipe-8781774',
    'https://www.allrecipes.com/baked-butter-beans-recipe-8782057'
]

for url in get_recipe_urls(start_url, num_recipes=100):
  print(url)
  try:
    recipe_data = scrape_recipe_data(url)
    create_recipe_in_db(recipe_data)
  except Exception as e:
    print(f'Error scraping recipe {url}: {e}')