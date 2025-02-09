from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Recipe, Category, Tag, Ingredient, RecipeIngredient
from .serializers import (
    RecipeSerializer,
    CategorySerializer,
    TagSerializer,
    IngredientSerializer,
    RecipeIngredientSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class RecipeIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['recipe', 'ingredient']

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()  # Default queryset, will be overridden by get_queryset
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'tags', 'is_shared_globally']
    search_fields = ['name', 'instructions']
    ordering_fields = ['name', 'prep_time', 'cook_time']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Return recipes that are either shared globally or added by the user
            return Recipe.objects.filter(
                Q(is_shared_globally=True) | Q(added_by=user)
            ).distinct()
        # For anonymous users, only return globally shared recipes
        return Recipe.objects.filter(is_shared_globally=True)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)