from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    assigned_to = models.CharField(max_length=100)

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
