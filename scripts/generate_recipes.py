import json
import random
from datetime import datetime, timedelta

# Recipe templates
breakfast_recipes = [
    {
        "name": "Classic Pancakes",
        "ingredients": "- 1 1/2 cups flour\n- 3 1/2 tsp baking powder\n- 1/4 tsp salt\n- 1 tbsp sugar\n- 1 1/4 cups milk\n- 1 egg\n- 3 tbsp butter, melted",
        "instructions": "1. Mix dry ingredients\n2. Whisk wet ingredients\n3. Combine until just mixed\n4. Cook on griddle\n5. Serve with maple syrup"
    },
    {
        "name": "Eggs Benedict",
        "ingredients": "- 4 English muffins\n- 8 eggs\n- 8 slices Canadian bacon\n- Hollandaise sauce\n- Chives for garnish",
        "instructions": "1. Toast muffins\n2. Poach eggs\n3. Warm Canadian bacon\n4. Make hollandaise\n5. Assemble and serve"
    },
    {
        "name": "Breakfast Burrito",
        "ingredients": "- Large tortillas\n- Scrambled eggs\n- Breakfast sausage\n- Cheese\n- Salsa\n- Avocado",
        "instructions": "1. Cook sausage\n2. Scramble eggs\n3. Warm tortillas\n4. Assemble burritos\n5. Serve with salsa"
    }
]

lunch_recipes = [
    {
        "name": "Chicken Caesar Salad",
        "ingredients": "- Romaine lettuce\n- Grilled chicken breast\n- Parmesan cheese\n- Croutons\n- Caesar dressing",
        "instructions": "1. Grill chicken\n2. Chop lettuce\n3. Combine ingredients\n4. Toss with dressing"
    },
    {
        "name": "Turkey Club Sandwich",
        "ingredients": "- Sliced turkey\n- Bacon\n- Lettuce\n- Tomato\n- Mayo\n- Bread",
        "instructions": "1. Cook bacon\n2. Toast bread\n3. Layer ingredients\n4. Cut and serve"
    },
    {
        "name": "Quinoa Bowl",
        "ingredients": "- Quinoa\n- Roasted vegetables\n- Chickpeas\n- Feta cheese\n- Lemon dressing",
        "instructions": "1. Cook quinoa\n2. Roast vegetables\n3. Season chickpeas\n4. Assemble bowl"
    }
]

dinner_recipes = [
    {
        "name": "Beef Stir Fry",
        "ingredients": "- Sliced beef\n- Mixed vegetables\n- Soy sauce\n- Garlic and ginger\n- Rice",
        "instructions": "1. Cook rice\n2. Stir fry beef\n3. Add vegetables\n4. Season and serve"
    },
    {
        "name": "Baked Salmon",
        "ingredients": "- Salmon fillets\n- Lemon\n- Garlic\n- Herbs\n- Olive oil",
        "instructions": "1. Preheat oven\n2. Season salmon\n3. Bake 12-15 mins\n4. Rest and serve"
    },
    {
        "name": "Vegetable Lasagna",
        "ingredients": "- Lasagna noodles\n- Ricotta cheese\n- Spinach\n- Marinara sauce\n- Mozzarella",
        "instructions": "1. Layer noodles\n2. Add cheese mixture\n3. Add vegetables\n4. Bake until bubbly"
    }
]

dessert_recipes = [
    {
        "name": "Apple Pie",
        "ingredients": "- Pie crust\n- Apples\n- Sugar\n- Cinnamon\n- Butter",
        "instructions": "1. Prepare crust\n2. Mix filling\n3. Assemble pie\n4. Bake until golden"
    },
    {
        "name": "Chocolate Mousse",
        "ingredients": "- Dark chocolate\n- Heavy cream\n- Eggs\n- Sugar\n- Vanilla",
        "instructions": "1. Melt chocolate\n2. Whip cream\n3. Fold together\n4. Chill and serve"
    },
    {
        "name": "Tiramisu",
        "ingredients": "- Ladyfingers\n- Mascarpone\n- Coffee\n- Cocoa powder\n- Eggs",
        "instructions": "1. Dip cookies\n2. Make cream\n3. Layer dessert\n4. Chill overnight"
    }
]

snack_recipes = [
    {
        "name": "Trail Mix",
        "ingredients": "- Mixed nuts\n- Dried fruit\n- Dark chocolate\n- Seeds\n- Coconut flakes",
        "instructions": "1. Combine ingredients\n2. Store in airtight container"
    },
    {
        "name": "Fruit Smoothie",
        "ingredients": "- Mixed berries\n- Banana\n- Yogurt\n- Honey\n- Ice",
        "instructions": "1. Blend fruit\n2. Add yogurt\n3. Sweeten to taste"
    }
]

def generate_variations(base_recipes, num_variations=5):
    """Generate variations of base recipes"""
    variations = []
    
    adjectives = ["Homestyle", "Gourmet", "Quick", "Easy", "Healthy", "Traditional", 
                 "Modern", "Spicy", "Seasonal", "Family", "Rustic", "Simple"]
    
    for recipe in base_recipes:
        for i in range(num_variations):
            new_recipe = recipe.copy()
            new_recipe["name"] = f"{random.choice(adjectives)} {recipe['name']}"
            variations.append(new_recipe)
    
    return variations

def generate_recipe(template, index):
    """Generate a recipe from a template"""
    recipe = {
        "model": "api.recipe",
        "pk": index,
        "fields": {
            "name": template["name"],
            "ingredients": template["ingredients"],
            "instructions": template["instructions"]
        }
    }
    return recipe

# Generate recipes
recipes = []
current_pk = 1

# Keep existing recipes (first 10)
with open('backend/api/fixtures/recipe_data.json', 'r') as f:
    existing_recipes = json.load(f)
    recipes.extend(existing_recipes)
    current_pk = max(r["pk"] for r in existing_recipes) + 1

# Generate variations of all recipes
all_base_recipes = (breakfast_recipes + lunch_recipes + dinner_recipes + 
                   dessert_recipes + snack_recipes)
all_variations = generate_variations(all_base_recipes, num_variations=7)

# Add new recipes
for template in all_variations:
    recipe = generate_recipe(template, current_pk)
    recipes.append(recipe)
    current_pk += 1

# Write to file
with open('backend/api/fixtures/recipe_data.json', 'w') as f:
    json.dump(recipes, f, indent=4)
