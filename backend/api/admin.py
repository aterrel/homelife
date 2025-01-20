from django.contrib import admin
from .models import Event, Recipe, Ingredient, RecipeIngredient

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
