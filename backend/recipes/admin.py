from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Category, Tag, RecipeCatalog

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'prep_time', 'cook_time', 'servings', 'is_shared_globally')
    search_fields = ('name',)
    list_filter = ('categories', 'tags')

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(RecipeCatalog)
class RecipeCatalogAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
