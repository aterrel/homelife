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

class Home(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return self.name

class Person(models.Model):
    home = models.ForeignKey(Home, related_name='people', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.name

class Chore(models.Model):
    home = models.ForeignKey(Home, related_name='chores', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(Person, related_name='chores', null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    home = models.ForeignKey(Home, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.title} on {self.date}"

class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

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
    added_by = models.ForeignKey(User, related_name='recipes', on_delete=models.CASCADE, blank=True, null=True)
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
        return f"{self.quantity} {self.get_units_display()} of {self.ingredient.name}"

class RecipeCatalog(models.Model):
    recipes = models.ManyToManyField(Recipe, related_name='catalogs')

    def __str__(self):
        return f"Catalog with {self.recipes.count()} recipes"

class Meal(models.Model):
    home = models.ForeignKey(Home, related_name='meals', on_delete=models.CASCADE)
    date = models.DateField()
    recipes = models.ManyToManyField(Recipe, related_name='meals')
    raw_ingredients = models.ManyToManyField(Ingredient, through='MealIngredient')
    people = models.ManyToManyField(Person, related_name='meals')
    guests = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Meal on {self.date}"

class MealIngredient(models.Model):
    meal = models.ForeignKey(Meal, related_name='meal_ingredients', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, related_name='meal_ingredients', on_delete=models.CASCADE)
    quantity = models.FloatField()
    units = models.CharField(max_length=50, choices=UNIT_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} {self.get_units_display()} of {self.ingredient.name} for {self.meal}"

class ShoppingList(models.Model):
    home = models.ForeignKey(Home, related_name='shopping_lists', on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    items = models.TextField()

    def __str__(self):
        return f"Shopping List created on {self.date_created}"
