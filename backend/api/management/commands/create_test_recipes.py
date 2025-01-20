from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Recipe, Ingredient, RecipeIngredient
from decimal import Decimal

class Command(BaseCommand):
    help = 'Creates test recipes for development'

    def handle(self, *args, **options):
        # Create test user if it doesn't exist
        user, created = User.objects.get_or_create(
            username='test_user',
            defaults={
                'email': 'test@example.com',
                'is_active': True,
            }
        )
        if created:
            user.set_password('test123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Create test recipes
        recipes_data = [
            {
                'name': 'Classic Chocolate Chip Cookies',
                'description': 'Delicious homemade chocolate chip cookies that are crispy on the outside and chewy on the inside.',
                'instructions': '1. Preheat oven to 375°F\n2. Cream butter and sugars\n3. Add eggs and vanilla\n4. Mix in dry ingredients\n5. Stir in chocolate chips\n6. Bake for 10-12 minutes',
                'prep_time': 15,
                'cook_time': 12,
                'servings': 24,
                'ingredients': [
                    ('all-purpose flour', 2.25, 'cup'),
                    ('butter', 1, 'cup'),
                    ('brown sugar', 0.75, 'cup'),
                    ('granulated sugar', 0.75, 'cup'),
                    ('eggs', 2, 'whole'),
                    ('vanilla extract', 1, 'tsp'),
                    ('chocolate chips', 2, 'cup'),
                    ('baking soda', 1, 'tsp'),
                    ('salt', 0.5, 'tsp'),
                ]
            },
            {
                'name': 'Simple Tomato Pasta',
                'description': 'Quick and easy pasta with fresh tomato sauce.',
                'instructions': '1. Boil pasta according to package directions\n2. Sauté garlic in olive oil\n3. Add tomatoes and cook until soft\n4. Season with salt and herbs\n5. Toss with pasta',
                'prep_time': 10,
                'cook_time': 20,
                'servings': 4,
                'ingredients': [
                    ('spaghetti', 1, 'pound'),
                    ('olive oil', 0.25, 'cup'),
                    ('garlic', 4, 'clove'),
                    ('tomatoes', 4, 'whole'),
                    ('basil', 0.25, 'cup'),
                    ('salt', 1, 'tsp'),
                    ('black pepper', 0.5, 'tsp'),
                ]
            }
        ]

        for recipe_data in recipes_data:
            ingredients = recipe_data.pop('ingredients')
            recipe = Recipe.objects.create(user=user, **recipe_data)
            
            for ing_name, quantity, unit in ingredients:
                ingredient, _ = Ingredient.objects.get_or_create(
                    name=ing_name.lower(),
                    defaults={'category': 'other'}
                )
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=Decimal(str(quantity)),
                    unit=unit
                )
            
            self.stdout.write(self.style.SUCCESS(f'Created recipe: {recipe.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully created test recipes'))
