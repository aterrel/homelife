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
        
        # Sample HTML from Minimalist Baker's cinnamon rolls recipe
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>The World's Easiest Cinnamon Rolls | Minimalist Baker Recipes</title>
            <meta name="description" content="The easiest cinnamon rolls you'll ever make.">
            <script type="application/ld+json">
            {
                "@context": "http://schema.org/",
                "@type": "Recipe",
                "name": "The World's Easiest Cinnamon Rolls",
                "description": "The easiest cinnamon rolls you'll ever make. Just 7 ingredients required and ready in less than 1 hour!",
                "author": {
                    "@type": "Person",
                    "name": "Minimalist Baker"
                },
                "prepTime": "PT15M",
                "cookTime": "PT25M",
                "totalTime": "PT40M",
                "recipeYield": "7",
                "recipeIngredient": [
                    "2 3/4 - 3 1/4 cups unbleached all-purpose flour",
                    "3 Tbsp granulated sugar",
                    "1 tsp salt",
                    "1 package instant yeast (2 1/4 tsp)",
                    "1/2 cup water",
                    "1/4 cup almond milk",
                    "2 Tbsp butter",
                    "1 large egg"
                ],
                "recipeInstructions": [
                    "In a large mixing bowl, combine 2 cups flour, sugar, salt, and yeast.",
                    "In a separate mixing bowl, microwave water, almond milk, and butter until warm.",
                    "Add wet ingredients to dry ingredients and mix well. Add egg and stir.",
                    "Gradually add remaining flour and knead for about 5 minutes.",
                    "Let dough rest for 10 minutes."
                ]
            }
            </script>
        </head>
        <body>
            <div class="wprm-recipe-container">
                <h2 class="wprm-recipe-name">The World's Easiest Cinnamon Rolls</h2>
                <div class="wprm-recipe-summary">
                    The easiest cinnamon rolls you'll ever make. Just 7 ingredients required and ready in less than 1 hour!
                </div>
                <div class="wprm-recipe-meta-container">
                    <div class="wprm-recipe-times-container">
                        <div class="wprm-recipe-prep-time-container">
                            <span class="wprm-recipe-time">15</span> minutes
                        </div>
                        <div class="wprm-recipe-cook-time-container">
                            <span class="wprm-recipe-time">25</span> minutes
                        </div>
                    </div>
                    <div class="wprm-recipe-servings-container">
                        <span class="wprm-recipe-servings">7</span> rolls
                    </div>
                </div>
                <div class="wprm-recipe-ingredients-container">
                    <h3>Ingredients</h3>
                    <ul>
                        <li>2 3/4 - 3 1/4 cups unbleached all-purpose flour</li>
                        <li>3 Tbsp granulated sugar</li>
                        <li>1 tsp salt</li>
                        <li>1 package instant yeast (2 1/4 tsp)</li>
                        <li>1/2 cup water</li>
                        <li>1/4 cup almond milk</li>
                        <li>2 Tbsp butter</li>
                        <li>1 large egg</li>
                    </ul>
                </div>
            </div>
        </body>
        </html>
        """

    @patch('api.services.requests.get')
    def test_recipe_scraping(self, mock_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.text = self.sample_html
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Test recipe scraping
        recipe = scrape_recipe('https://minimalistbaker.com/the-worlds-easiest-cinnamon-rolls/', self.user)

        # Check basic recipe information
        self.assertEqual(recipe.name, "The World's Easiest Cinnamon Rolls")
        self.assertTrue("easiest cinnamon rolls you'll ever make" in recipe.description.lower())
        self.assertEqual(recipe.prep_time, 15)
        self.assertEqual(recipe.cook_time, 25)
        self.assertEqual(recipe.servings, 7)

        # Check ingredients
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        self.assertTrue(ingredients.exists())

        # Check specific ingredients
        ingredient_checks = [
            ('flour', Decimal('2.75'), 'cup'),  # Testing the first measurement of the range
            ('sugar', Decimal('3'), 'tbsp'),
            ('salt', Decimal('1'), 'tsp'),
            ('yeast', Decimal('1'), 'package'),
            ('water', Decimal('0.5'), 'cup'),
            ('milk', Decimal('0.25'), 'cup'),
            ('butter', Decimal('2'), 'tbsp'),
            ('egg', Decimal('1'), 'whole'),
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
        test_cases = [
            (
                "2 3/4 cups unbleached all-purpose flour",
                ("unbleached all-purpose flour", Decimal('2.75'), "cup", "")
            ),
            (
                "3 Tbsp granulated sugar",
                ("granulated sugar", Decimal('3'), "tbsp", "")
            ),
            (
                "1/2 - 1 Tbsp ground cinnamon",
                ("ground cinnamon", Decimal('0.5'), "tbsp", "")  # Takes the first number
            ),
            (
                "1 large egg",
                ("large egg", Decimal('1'), "whole", "")
            ),
            (
                "2 Tbsp butter (melted)",
                ("butter", Decimal('2'), "tbsp", "melted")
            ),
            (
                "1/4 cup almond milk",
                ("almond milk", Decimal('0.25'), "cup", "")
            ),
            (
                "1 package instant yeast (2 1/4 tsp)",
                ("instant yeast", Decimal('1'), "package", "2 1/4 tsp")
            ),
        ]

        for input_line, expected in test_cases:
            name, quantity, unit, notes = parse_ingredient_line(input_line)
            self.assertEqual(
                (name.lower(), quantity, unit.lower(), notes.lower()),
                (expected[0].lower(), expected[1], expected[2].lower(), expected[3].lower()),
                f"Failed parsing: {input_line}"
            )
