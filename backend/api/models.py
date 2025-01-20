from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} on {self.date} at {self.time}"

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[
        ('dairy', 'Dairy'),
        ('meat', 'Meat'),
        ('produce', 'Produce'),
        ('pantry', 'Pantry'),
        ('spices', 'Spices'),
        ('other', 'Other')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()
    prep_time = models.IntegerField(help_text="Preparation time in minutes", default=0)
    cook_time = models.IntegerField(help_text="Cooking time in minutes", default=0)
    servings = models.IntegerField(default=4)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=50, choices=[
        ('g', 'Grams'),
        ('kg', 'Kilograms'),
        ('oz', 'Ounces'),
        ('lb', 'Pounds'),
        ('cup', 'Cups'),
        ('tbsp', 'Tablespoons'),
        ('tsp', 'Teaspoons'),
        ('ml', 'Milliliters'),
        ('l', 'Liters'),
        ('piece', 'Pieces'),
        ('pinch', 'Pinch'),
        ('whole', 'Whole'),
        ('to_taste', 'To Taste')
    ])
    optional = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.quantity} {self.unit} {self.ingredient.name}"

    class Meta:
        ordering = ['order', 'id']
