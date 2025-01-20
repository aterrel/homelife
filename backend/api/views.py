from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Event, Recipe, Ingredient, RecipeIngredient
from .serializers import EventSerializer, RecipeSerializer, UserSerializer
from .services import scrape_recipe
from .authentication import TestTokenAuthentication
import requests
import logging

logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TestTokenAuthentication]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TestTokenAuthentication]

    def get_queryset(self):
        logger.debug(f"Getting recipes for user: {self.request.user}")
        recipes = Recipe.objects.filter(user=self.request.user)
        logger.debug(f"Found {recipes.count()} recipes")
        return recipes

    def list(self, request, *args, **kwargs):
        logger.debug(f"Recipe list request from user: {request.user}")
        logger.debug(f"Auth header: {request.headers.get('Authorization')}")
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['post'])
    def import_from_url(self, request):
        """Import a recipe from a URL"""
        url = request.data.get('url')
        if not url:
            return Response(
                {'error': 'URL is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            recipe = scrape_recipe(url, request.user)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []  # No authentication needed for registration
