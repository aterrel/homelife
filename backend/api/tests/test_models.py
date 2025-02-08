from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from api.models import Event, Recipe, Ingredient, RecipeIngredient, MealPlan, MealSlot
from decimal import Decimal
from django.core.exceptions import ValidationError

class EventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.event = Event.objects.create(
            title='Test Event',
            date='2025-01-21',
            time='14:30:00',
            user=self.user
        )

    def test_event_creation(self):
        """Test that an event can be created with all required fields"""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(str(self.event.date), '2025-01-21')
        self.assertEqual(str(self.event.time), '14:30:00')
        self.assertEqual(self.event.user, self.user)

    def test_event_str_method(self):
        """Test the string representation of an event"""
        expected_str = 'Test Event on 2025-01-21 at 14:30:00'
        self.assertEqual(str(self.event), expected_str)

    def test_event_timestamps(self):
        """Test that created_at and updated_at are set"""
        self.assertIsNotNone(self.event.created_at)
        self.assertIsNotNone(self.event.updated_at)

class IngredientModelTests(TestCase):
    def setUp(self):
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            description='Test Description',
            category='produce'
        )

    def test_ingredient_creation(self):
        """Test that an ingredient can be created with all fields"""
        self.assertEqual(self.ingredient.name, 'Test Ingredient')
        self.assertEqual(self.ingredient.description, 'Test Description')
        self.assertEqual(self.ingredient.category, 'produce')

    def test_ingredient_str_method(self):
        """Test the string representation of an ingredient"""
        self.assertEqual(str(self.ingredient), 'Test Ingredient')

    def test_ingredient_category_choices(self):
        """Test that invalid category choices are rejected"""
        with self.assertRaises(ValidationError):
            ingredient = Ingredient(
                name='Invalid Category',
                category='invalid_category'
            )
            ingredient.clean()

class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            instructions='Test Instructions',
            prep_time=15,
            cook_time=30,
            servings=4,
            difficulty='medium',
            user=self.user
        )

    def test_recipe_creation(self):
        """Test that a recipe can be created with all fields"""
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.description, 'Test Description')
        self.assertEqual(self.recipe.instructions, 'Test Instructions')
        self.assertEqual(self.recipe.prep_time, 15)
        self.assertEqual(self.recipe.cook_time, 30)
        self.assertEqual(self.recipe.servings, 4)
        self.assertEqual(self.recipe.difficulty, 'medium')
        self.assertEqual(self.recipe.user, self.user)

    def test_recipe_timestamps(self):
        """Test that created_at and updated_at are set"""
        self.assertIsNotNone(self.recipe.created_at)
        self.assertIsNotNone(self.recipe.updated_at)

    def test_recipe_difficulty_choices(self):
        """Test that invalid difficulty choices are rejected"""
        with self.assertRaises(Exception):
            Recipe.objects.create(
                name='Invalid Difficulty',
                instructions='Test',
                difficulty='invalid_difficulty',
                user=self.user
            )

class RecipeIngredientModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            instructions='Test Instructions',
            user=self.user
        )
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            category='produce'
        )
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=Decimal('2.5'),
            unit='cup',
            notes='Test notes',
            order=1
        )

    def test_recipe_ingredient_creation(self):
        """Test that a recipe ingredient can be created with all fields"""
        self.assertEqual(self.recipe_ingredient.recipe, self.recipe)
        self.assertEqual(self.recipe_ingredient.ingredient, self.ingredient)
        self.assertEqual(self.recipe_ingredient.quantity, Decimal('2.5'))
        self.assertEqual(self.recipe_ingredient.unit, 'cup')
        self.assertEqual(self.recipe_ingredient.notes, 'Test notes')
        self.assertEqual(self.recipe_ingredient.order, 1)

    def test_recipe_ingredient_str_method(self):
        """Test the string representation of a recipe ingredient"""
        expected_str = f'{self.recipe.name} - {self.ingredient.name}'
        self.assertEqual(str(self.recipe_ingredient), expected_str)

    def test_recipe_ingredient_unit_choices(self):
        """Test that invalid unit choices are rejected"""
        with self.assertRaises(Exception):
            RecipeIngredient.objects.create(
                recipe=self.recipe,
                ingredient=self.ingredient,
                quantity=1,
                unit='invalid_unit'
            )

    def test_recipe_ingredient_ordering(self):
        """Test that recipe ingredients are ordered by order field"""
        # Create another recipe ingredient with lower order
        recipe_ingredient2 = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity=1,
            unit='cup',
            order=0
        )
        
        # Get ordered recipe ingredients
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=self.recipe)
        self.assertEqual(recipe_ingredients[0], recipe_ingredient2)  # order=0 should come first
        self.assertEqual(recipe_ingredients[1], self.recipe_ingredient)  # order=1 should come second

class MealPlanModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mealplanner',
            password='testpass123'
        )
        self.meal_plan = MealPlan.objects.create(
            user=self.user,
            start_date='2025-02-01',
            name='Test Meal Plan',
            notes='Test Notes'
        )

    def test_meal_plan_creation(self):
        """Test that a meal plan can be created with all fields"""
        self.assertEqual(self.meal_plan.name, 'Test Meal Plan')
        self.assertEqual(str(self.meal_plan.start_date), '2025-02-01')
        self.assertEqual(self.meal_plan.notes, 'Test Notes')
        self.assertEqual(self.meal_plan.user, self.user)

    def test_meal_plan_str_method(self):
        """Test the string representation of a meal plan"""
        expected_str = 'Test Meal Plan - Starting 2025-02-01'
        self.assertEqual(str(self.meal_plan), expected_str)

    def test_meal_plan_timestamps(self):
        """Test that created_at and updated_at are set"""
        self.assertIsNotNone(self.meal_plan.created_at)
        self.assertIsNotNone(self.meal_plan.updated_at)

    def test_meal_plan_ordering(self):
        """Test that meal plans are ordered by start_date in descending order"""
        MealPlan.objects.create(
            user=self.user,
            start_date='2025-02-08',
            name='Later Plan'
        )
        MealPlan.objects.create(
            user=self.user,
            start_date='2025-01-25',
            name='Earlier Plan'
        )
        plans = MealPlan.objects.all()
        self.assertEqual(plans[0].start_date.isoformat(), '2025-02-08')
        self.assertEqual(plans[1].start_date.isoformat(), '2025-02-01')
        self.assertEqual(plans[2].start_date.isoformat(), '2025-01-25')

class MealSlotModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mealplanner',
            password='testpass123'
        )
        self.meal_plan = MealPlan.objects.create(
            user=self.user,
            start_date='2025-02-01',
            name='Test Meal Plan'
        )
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            description='Test Description',
            instructions='Test Instructions',
            prep_time=30,
            cook_time=45,
            servings=4,
            difficulty='medium',
            user=self.user
        )
        self.meal_slot = MealSlot.objects.create(
            meal_plan=self.meal_plan,
            recipe=self.recipe,
            date='2025-02-01',
            meal_type='breakfast',
            notes='Test Notes',
            servings=2
        )

    def test_meal_slot_creation(self):
        """Test that a meal slot can be created with all fields"""
        self.assertEqual(self.meal_slot.meal_plan, self.meal_plan)
        self.assertEqual(self.meal_slot.recipe, self.recipe)
        self.assertEqual(str(self.meal_slot.date), '2025-02-01')
        self.assertEqual(self.meal_slot.meal_type, 'breakfast')
        self.assertEqual(self.meal_slot.notes, 'Test Notes')
        self.assertEqual(self.meal_slot.servings, 2)

    def test_meal_slot_str_method(self):
        """Test the string representation of a meal slot"""
        expected_str = 'Breakfast - Test Recipe (2025-02-01)'
        self.assertEqual(str(self.meal_slot), expected_str)

    def test_meal_slot_timestamps(self):
        """Test that created_at and updated_at are set"""
        self.assertIsNotNone(self.meal_slot.created_at)
        self.assertIsNotNone(self.meal_slot.updated_at)

    def test_meal_slot_optional_recipe(self):
        """Test that a meal slot can be created without a recipe"""
        slot = MealSlot.objects.create(
            meal_plan=self.meal_plan,
            date='2025-02-01',
            meal_type='lunch'
        )
        self.assertIsNone(slot.recipe)
        self.assertEqual(str(slot), 'Lunch - No recipe (2025-02-01)')

    def test_meal_slot_unique_constraint(self):
        """Test that a meal slot must be unique for meal_plan, date, and meal_type"""
        with self.assertRaises(Exception):
            MealSlot.objects.create(
                meal_plan=self.meal_plan,
                date='2025-02-01',
                meal_type='breakfast'
            )

    def test_meal_slot_meal_type_choices(self):
        """Test that invalid meal types are rejected"""
        with self.assertRaises(ValidationError):
            slot = MealSlot(
                meal_plan=self.meal_plan,
                date='2025-02-01',
                meal_type='invalid_type'
            )
            slot.full_clean()

    def test_meal_slot_ordering(self):
        """Test that meal slots are ordered by date and meal type"""
        lunch = MealSlot.objects.create(
            meal_plan=self.meal_plan,
            date='2025-02-01',
            meal_type='lunch'
        )
        dinner = MealSlot.objects.create(
            meal_plan=self.meal_plan,
            date='2025-02-01',
            meal_type='dinner'
        )
        next_breakfast = MealSlot.objects.create(
            meal_plan=self.meal_plan,
            date='2025-02-02',
            meal_type='breakfast'
        )
        
        slots = list(MealSlot.objects.all())
        self.assertEqual(slots[0], self.meal_slot)  # breakfast on 2025-02-01
        self.assertEqual(slots[1], lunch)           # lunch on 2025-02-01
        self.assertEqual(slots[2], dinner)          # dinner on 2025-02-01
        self.assertEqual(slots[3], next_breakfast)  # breakfast on 2025-02-02
