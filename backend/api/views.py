from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from .models import Event, Recipe, Ingredient, RecipeIngredient, MealPlan, MealSlot
from .serializers import EventSerializer, RecipeSerializer, UserSerializer, MealPlanSerializer, MealSlotSerializer
from .services import scrape_recipe
import requests
import logging

logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        logger.debug(f"Getting recipes for user: {self.request.user}")
        recipes = Recipe.objects.all()
        logger.debug(f"Found {recipes.count()} recipes")
        return recipes

    def create(self, request, *args, **kwargs):
        logger.debug(f"Creating recipe with data: {request.data}")
        ingredients_data = request.data.pop('ingredients', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save(user=self.request.user)
        
        # Handle ingredients
        self._handle_ingredients(recipe, ingredients_data)
        
        # Get updated recipe data
        updated_serializer = self.get_serializer(recipe)
        return Response(updated_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating recipe with data: {request.data}")
        data = request.data.copy()  # Create a mutable copy
        ingredients_data = data.pop('ingredients', [])
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        # Clear existing ingredients and add new ones
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        self._handle_ingredients(recipe, ingredients_data)

        # Get updated recipe data
        updated_serializer = self.get_serializer(recipe)
        return Response(updated_serializer.data)

    def _handle_ingredients(self, recipe, ingredients_data):
        """Helper method to handle ingredient creation and linking"""
        logger.debug(f"Handling ingredients for recipe {recipe.id}: {ingredients_data}")
        
        for ing_data in ingredients_data:
            ingredient_info = ing_data.get('ingredient', {})
            
            # Get or create the ingredient
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_info['name'].lower(),
                defaults={'category': 'other'}
            )
            
            # Create the recipe-ingredient relationship
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ing_data.get('quantity', 0),
                unit=ing_data.get('unit', ''),
                notes=ing_data.get('notes', '')
            )
        
    def list(self, request, *args, **kwargs):
        logger.debug(f"Recipe list request from user: {request.user}")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['post'])
    def import_from_url(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            recipe_data = scrape_recipe(url)
            recipe_data['user'] = request.user.id
            serializer = self.get_serializer(data=recipe_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MealPlanViewSet(viewsets.ModelViewSet):
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return MealPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def bulk_create_slots(self, request, pk=None):
        meal_plan = self.get_object()
        slots_data = request.data.get('slots', [])
        
        created_slots = []
        for slot_data in slots_data:
            slot_data['meal_plan'] = meal_plan.id
            serializer = MealSlotSerializer(data=slot_data)
            if serializer.is_valid():
                slot = serializer.save()
                created_slots.append(slot)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(MealSlotSerializer(created_slots, many=True).data, status=status.HTTP_201_CREATED)

class MealSlotViewSet(viewsets.ModelViewSet):
    serializer_class = MealSlotSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return MealSlot.objects.filter(meal_plan__user=self.request.user)

    def perform_create(self, serializer):
        meal_plan = serializer.validated_data['meal_plan']
        if meal_plan.user != self.request.user:
            raise PermissionError("You don't have permission to add slots to this meal plan")
        serializer.save()

class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []  # No authentication needed for registration
