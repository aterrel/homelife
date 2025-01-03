from django.test import TestCase

from .models import Event, Recipe

class EventTestCase(TestCase):
    fixtures = ['event_data.json']

    def test_event(self):
        event = Event.objects.get(title='Soccer Practice')
        self.assertEqual(event.assigned_to, 'Mom')

class RecipeTestCase(TestCase):
    fixtures = ['recipe_data.json']

    def test_recipe(self):
        recipe = Recipe.objects.get(name='Spaghetti')
        self.assertIsNotNone(recipe.ingredients)

