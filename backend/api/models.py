from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
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
    CATEGORY_CHOICES = [
        ('produce', 'Produce'),
        ('meat', 'Meat'),
        ('dairy', 'Dairy'),
        ('pantry', 'Pantry'),
        ('spices', 'Spices'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.category not in dict(self.CATEGORY_CHOICES):
            raise ValidationError({'category': 'Invalid category choice'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructions = models.TextField()
    prep_time = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    cook_time = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    servings = models.IntegerField(validators=[MinValueValidator(1)], null=True, blank=True)
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.difficulty and self.difficulty not in dict(self.DIFFICULTY_CHOICES):
            raise ValidationError({'difficulty': 'Invalid difficulty choice'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class RecipeIngredient(models.Model):
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

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
    notes = models.TextField(blank=True)
    optional = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def clean(self):
        if self.unit not in dict(self.UNIT_CHOICES):
            raise ValidationError({'unit': 'Invalid unit choice'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    start_date = models.DateField()
    name = models.CharField(max_length=200, default="Weekly Meal Plan")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Starting {self.start_date}"

    class Meta:
        ordering = ['-start_date']

class MealSlot(models.Model):
    MEAL_TYPE_ORDER = {
        'breakfast': 1,
        'lunch': 2,
        'dinner': 3,
        'snack': 4
    }
    
    MEAL_TYPE_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meal_slots')
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    meal_type_order = models.IntegerField(editable=False)
    notes = models.TextField(blank=True)
    servings = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.meal_type_order = self.MEAL_TYPE_ORDER.get(self.meal_type, 5)
        super().save(*args, **kwargs)

    def __str__(self):
        recipe_name = self.recipe.name if self.recipe else "No recipe"
        return f"{self.get_meal_type_display()} - {recipe_name} ({self.date})"

    class Meta:
        ordering = ['date', 'meal_type_order']
        unique_together = ['meal_plan', 'date', 'meal_type']
