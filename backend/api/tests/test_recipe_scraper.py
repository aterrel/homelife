from django.test import TestCase
from django.contrib.auth.models import User
from api.services import scrape_recipe, parse_ingredient_line
from api.models import Recipe, Ingredient, RecipeIngredient
from unittest.mock import patch, MagicMock
from decimal import Decimal

class TestRecipeScraper(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.html_content = """
        <html>
            <head>
                <title>Pizza Dough</title>
            </head>
            <body>
                <h1>Pizza Dough</h1>
                <div class="recipe-ingredients">
                    <ul>
                        <li>3 cups all-purpose flour</li>
                        <li>1 tsp salt</li>
                        <li>1 package instant yeast (2 1/4 tsp)</li>
                        <li>1 cup warm water</li>
                        <li>2 tbsp olive oil</li>
                    </ul>
                </div>
                <div class="recipe-instructions">
                    <ol>
                        <li>Mix flour and salt</li>
                        <li>Add yeast to warm water</li>
                        <li>Mix wet and dry ingredients</li>
                        <li>Knead dough for 10 minutes</li>
                        <li>Let rise for 1 hour</li>
                    </ol>
                </div>
            </body>
        </html>
        """

    @patch('api.services.requests.get')
    def test_recipe_scraping(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.text = self.html_content
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test recipe scraping
        recipe = scrape_recipe('https://example.com/recipe', self.user)

        # Check basic recipe information
        self.assertEqual(recipe.name, "Pizza Dough")
        self.assertEqual(recipe.description, "")

        # Check ingredients
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertTrue(ingredients.exists())

        # Check specific ingredients
        ingredient_checks = [
            ('flour', Decimal('3'), 'cup'),
            ('salt', Decimal('1'), 'tsp'),
            ('yeast', Decimal('1'), 'pkg'),
            ('water', Decimal('1'), 'cup'),
            ('oil', Decimal('2'), 'tbsp'),
        ]

        for name, expected_quantity, expected_unit in ingredient_checks:
            ingredient = ingredients.filter(ingredient__name__icontains=name).first()
            self.assertIsNotNone(
                ingredient,
                f"Ingredient containing '{name}' not found"
            )
            self.assertEqual(
                ingredient.quantity,
                expected_quantity,
                f"Quantity mismatch for {name}"
            )
            self.assertEqual(
                ingredient.unit.lower(),
                expected_unit.lower(),
                f"Unit mismatch for {name}"
            )

    def test_ingredient_parsing(self):
        """Test parsing individual ingredient lines"""
        test_cases = [
            (
                "1 cup flour",
                ("flour", 1.0, "cup", "")
            ),
            (
                "2 tablespoons sugar",
                ("sugar", 2.0, "tbsp", "")
            ),
            (
                "1/2 teaspoon salt",
                ("salt", 0.5, "tsp", "")
            ),
            (
                "1 package instant yeast (2 1/4 tsp)",
                ("instant yeast", 1.0, "pkg", "2 1/4 tsp")
            ),
            (
                "1 large egg",
                ("egg", 1.0, "whole", "")
            ),
            (
                "2 whole eggs",
                ("eggs", 2.0, "whole", "")
            ),
        ]

        for input_line, expected in test_cases:
            name, quantity, unit, notes = parse_ingredient_line(input_line)
            self.assertEqual(
                (name, quantity, unit, notes),
                expected,
                f"Failed parsing: {input_line}"
            )

    @patch('api.services.requests.get')
    def test_recipe_scraping(self, mock_get):
        """Test scraping a recipe from HTML"""
        # Mock the HTTP response
        mock_response = MagicMock()
        mock_response.text = self.html_content
        mock_get.return_value = mock_response

        # Scrape the recipe
        recipe_data = scrape_recipe('https://example.com/recipe', self.user)

        # Verify recipe data
        self.assertEqual(recipe_data['name'], 'Pizza Dough')
        self.assertEqual(len(recipe_data['ingredients']), 5)

        # Check specific ingredients
        ingredients = recipe_data['ingredients']
        flour = next((i for i in ingredients if 'flour' in i['ingredient']['name']), None)
        self.assertIsNotNone(flour, 'Ingredient containing "flour" not found')
        self.assertEqual(flour['unit'], 'cup')
        self.assertEqual(flour['quantity'], 3.0)

        salt = next((i for i in ingredients if 'salt' in i['ingredient']['name']), None)
        self.assertIsNotNone(salt, 'Ingredient containing "salt" not found')
        self.assertEqual(salt['unit'], 'tsp')
        self.assertEqual(salt['quantity'], 1.0)

        yeast = next((i for i in ingredients if 'yeast' in i['ingredient']['name']), None)
        self.assertIsNotNone(yeast, 'Ingredient containing "yeast" not found')
        self.assertEqual(yeast['unit'], 'pkg')
        self.assertEqual(yeast['quantity'], 1.0)

        water = next((i for i in ingredients if 'water' in i['ingredient']['name']), None)
        self.assertIsNotNone(water, 'Ingredient containing "water" not found')
        self.assertEqual(water['unit'], 'cup')
        self.assertEqual(water['quantity'], 1.0)

        oil = next((i for i in ingredients if 'oil' in i['ingredient']['name']), None)
        self.assertIsNotNone(oil, 'Ingredient containing "oil" not found')
        self.assertEqual(oil['unit'], 'tbsp')
        self.assertEqual(oil['quantity'], 2.0)

        # Check instructions
        self.assertIn('Mix flour and salt', recipe_data['instructions'])
