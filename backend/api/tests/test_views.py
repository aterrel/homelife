from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Event, Recipe, Ingredient, RecipeIngredient
from decimal import Decimal

class BaseAPITest(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        # Get tokens for user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

class EventViewSetTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Create test events
        self.event1 = Event.objects.create(
            title='User1 Event',
            date='2025-01-21',
            time='14:30:00',
            user=self.user1
        )
        self.event2 = Event.objects.create(
            title='User2 Event',
            date='2025-01-21',
            time='15:30:00',
            user=self.user2
        )

    def test_list_events(self):
        """Test that users can only see their own events"""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'User1 Event')

    def test_create_event(self):
        """Test event creation"""
        url = reverse('event-list')
        data = {
            'title': 'New Event',
            'date': '2025-01-22',
            'time': '16:30:00'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 3)
        self.assertEqual(Event.objects.filter(user=self.user1).count(), 2)

    def test_update_event(self):
        """Test event update"""
        url = reverse('event-detail', args=[self.event1.id])
        data = {
            'title': 'Updated Event'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=self.event1.id).title, 'Updated Event')

    def test_delete_event(self):
        """Test event deletion"""
        url = reverse('event-detail', args=[self.event1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.count(), 1)

class RecipeViewSetTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        # Create test recipes
        self.recipe1 = Recipe.objects.create(
            name='User1 Recipe',
            instructions='Test Instructions',
            user=self.user1
        )
        self.recipe2 = Recipe.objects.create(
            name='User2 Recipe',
            instructions='Test Instructions',
            user=self.user2
        )
        
        # Create test ingredients
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            category='produce'
        )

    def test_list_recipes(self):
        """Test that users can see all recipes"""
        url = reverse('recipe-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Should see both recipes

    def test_create_recipe(self):
        """Test recipe creation with ingredients"""
        url = reverse('recipe-list')
        data = {
            'name': 'New Recipe',
            'instructions': 'Test Instructions',
            'ingredients': [
                {
                    'ingredient': {
                        'name': 'New Ingredient',
                        'category': 'produce'
                    },
                    'quantity': '2.5',
                    'unit': 'cup',
                    'notes': 'Test notes'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recipe.objects.count(), 3)
        self.assertEqual(Ingredient.objects.count(), 2)
        self.assertEqual(RecipeIngredient.objects.count(), 1)

    def test_update_recipe(self):
        """Test recipe update"""
        url = reverse('recipe-detail', args=[self.recipe1.id])
        data = {
            'name': 'Updated Recipe'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Recipe.objects.get(id=self.recipe1.id).name, 'Updated Recipe')

    def test_delete_recipe(self):
        """Test recipe deletion"""
        url = reverse('recipe-detail', args=[self.recipe1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_import_recipe(self):
        """Test recipe import from URL"""
        url = reverse('recipe-import-from-url')
        data = {
            'url': 'https://example.com/recipe'
        }
        response = self.client.post(url, data)
        # Note: This will fail unless we mock the scrape_recipe function
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()

    def test_obtain_token(self):
        """Test obtaining JWT token"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        """Test refreshing JWT token"""
        # First obtain tokens
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        refresh_token = response.data['refresh']

        # Then try to refresh
        url = reverse('token_refresh')
        data = {
            'refresh': refresh_token
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_access_protected_view_without_token(self):
        """Test accessing protected view without token"""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
