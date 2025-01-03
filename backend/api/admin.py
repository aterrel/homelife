from django.contrib import admin
from .models import Event, Recipe

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'assigned_to')  # Fields to display in the admin list view
    search_fields = ('title', 'assigned_to')                # Fields to enable search functionality
    list_filter = ('date',)                                 # Add filters for the list view

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'ingredients')                  # Display recipe name and ingredients
    search_fields = ('name',)                               # Search by recipe name
    list_filter = ()                                        # You can add filters like tags here
