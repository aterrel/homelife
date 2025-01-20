from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Event, Recipe

class EventTestCase(TestCase):
    fixtures = ['test_users.json', 'event_data.json']

    def test_event(self):
        event = Event.objects.get(title='Soccer Practice')
        user = User.objects.get(username='testuser1')
        self.assertEqual(event.title, 'Soccer Practice')
        self.assertEqual(event.user, user)

class RecipeTestCase(TestCase):
    fixtures = ['recipe_data.json']

    def test_recipe(self):
        recipe = Recipe.objects.get(name='Spaghetti')
        self.assertIsNotNone(recipe.ingredients)

class UserRegistrationTests(APITestCase):
    fixtures = ['test_users.json']

    def test_user_registration(self):
        """Test that a new user can be created"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'testpass123',
            'password2': 'testpass123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # 2 from fixture + 1 new
        self.assertEqual(User.objects.get(username='newuser').email, 'newuser@example.com')

    def test_existing_user(self):
        """Test that existing username cannot register again"""
        url = reverse('register')
        data = {
            'username': 'testuser1',  # This username exists in fixture
            'password': 'testpass123',
            'password2': 'testpass123',
            'email': 'another@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
