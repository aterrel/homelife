from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe, Category, Tag, Ingredient, RecipeIngredient

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'quantity', 'units', 'notes', 'optional', 'order']

class RecipeSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        source='categories',
        write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True
    )
    recipe_ingredients = RecipeIngredientSerializer(many=True)
    added_by = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'prep_time', 'cook_time', 'servings',
            'instructions', 'url', 'categories', 'category_ids',
            'tags', 'tag_ids', 'recipe_ingredients', 'added_by',
            'is_shared_globally'
        ]

    def create(self, validated_data):
        categories = validated_data.pop('categories', [])
        tags = validated_data.pop('tags', [])
        recipe_ingredients_data = validated_data.pop('recipe_ingredients', [])

        recipe = Recipe.objects.create(**validated_data)
        recipe.categories.set(categories)
        recipe.tags.set(tags)

        for ingredient_data in recipe_ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe, **ingredient_data)

        return recipe

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        tags = validated_data.pop('tags', None)
        recipe_ingredients_data = validated_data.pop('recipe_ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if categories is not None:
            instance.categories.set(categories)
        if tags is not None:
            instance.tags.set(tags)
        if recipe_ingredients_data is not None:
            instance.recipe_ingredients.all().delete()
            for ingredient_data in recipe_ingredients_data:
                RecipeIngredient.objects.create(recipe=instance, **ingredient_data)

        return instance