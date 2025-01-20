from django.contrib import admin
from .models import Event, Recipe

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'user')
    list_filter = ('date', 'user')
    search_fields = ('title',)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
