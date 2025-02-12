from django.db import models
from django.contrib.auth.models import User

UNIT_CHOICES = [
    ('cup', 'Cup'),
    ('tbsp', 'Tablespoon'),
    ('tsp', 'Teaspoon'),
    ('oz', 'Ounce'),
    ('lb', 'Pound'),
    ('g', 'Gram'),
    ('kg', 'Kilogram'),
    ('ml', 'Milliliter'),
    ('l', 'Liter'),
    ('pinch', 'Pinch'),
    ('piece', 'Piece'),
    ('whole', 'Whole'),
    ('pkg', 'Package'),
    ('slice', 'Slice'),
]

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    prep_time = models.DurationField()
    cook_time = models.DurationField()
    servings = models.IntegerField()
    instructions = models.TextField()
    url = models.URLField(blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    added_by = models.ForeignKey(User, related_name='created_recipes', on_delete=models.CASCADE, blank=True, null=True)
    is_shared_globally = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='recipe_ingredients', on_delete=models.CASCADE)
    quantity = models.FloatField()
    units = models.CharField(max_length=50, choices=UNIT_CHOICES)
    notes = models.TextField(blank=True, null=True)
    optional = models.BooleanField(default=False)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.quantity} {self.units} {self.ingredient.name} for {self.recipe.name}'

class RecipeCatalog(models.Model):
    recipes = models.ManyToManyField(Recipe, related_name='catalogs')

    def __str__(self):
        return f'Recipe Catalog with {self.recipes.count()} recipes'
