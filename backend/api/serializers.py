from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Recipe, Ingredient, RecipeIngredient, MealPlan, MealSlot
from django.contrib.auth.password_validation import validate_password

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'time', 'user']
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'category']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
        write_only=True
    )
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_id', 'quantity', 'unit', 'optional', 'notes']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'instructions', 
            'prep_time', 'cook_time', 'servings', 'difficulty',
            'ingredients', 'user', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user']

class MealSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealSlot
        fields = ['id', 'meal_plan', 'recipe', 'date', 'meal_type', 'notes', 'servings', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MealPlanSerializer(serializers.ModelSerializer):
    meal_slots = MealSlotSerializer(many=True, read_only=True)

    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'start_date', 'name', 'notes', 'meal_slots', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'user']
