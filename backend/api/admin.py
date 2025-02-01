from django.contrib import admin
from .models import Event, Recipe, Ingredient, RecipeIngredient, MealPlan, MealSlot

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'user')
    list_filter = ('date', 'user')
    search_fields = ('title', 'user__username')

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'prep_time', 'cook_time', 'servings', 'user')
    list_filter = ('difficulty', 'user')
    search_fields = ('name', 'description', 'user__username')
    inlines = [RecipeIngredientInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'user')
        }),
        ('Instructions', {
            'fields': ('instructions',)
        }),
        ('Details', {
            'fields': ('prep_time', 'cook_time', 'servings', 'difficulty')
        }),
    )

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('name',)

class MealSlotInline(admin.TabularInline):
    model = MealSlot
    extra = 1
    autocomplete_fields = ['recipe']
    fields = ('date', 'meal_type', 'recipe', 'servings', 'notes')
    ordering = ('date', 'meal_type_order')

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'user', 'created_at')
    list_filter = ('start_date', 'user')
    search_fields = ('name', 'notes', 'user__username')
    inlines = [MealSlotInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'start_date', 'user')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    ordering = ('-start_date',)

@admin.register(MealSlot)
class MealSlotAdmin(admin.ModelAdmin):
    list_display = ('meal_plan', 'date', 'meal_type', 'recipe', 'servings')
    list_filter = ('date', 'meal_type', 'meal_plan__user')
    search_fields = ('meal_plan__name', 'recipe__name', 'notes')
    autocomplete_fields = ['recipe']
    raw_id_fields = ['meal_plan']
    ordering = ('date', 'meal_type_order')
    fieldsets = (
        (None, {
            'fields': ('meal_plan', 'date', 'meal_type', 'recipe')
        }),
        ('Details', {
            'fields': ('servings', 'notes')
        }),
    )
