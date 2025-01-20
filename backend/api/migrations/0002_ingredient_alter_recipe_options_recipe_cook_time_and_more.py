# Generated by Django 5.1.5 on 2025-01-20 12:31

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("dairy", "Dairy"),
                            ("meat", "Meat"),
                            ("produce", "Produce"),
                            ("pantry", "Pantry"),
                            ("spices", "Spices"),
                            ("other", "Other"),
                        ],
                        max_length=50,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AlterModelOptions(
            name="recipe",
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddField(
            model_name="recipe",
            name="cook_time",
            field=models.IntegerField(default=0, help_text="Cooking time in minutes"),
        ),
        migrations.AddField(
            model_name="recipe",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="difficulty",
            field=models.CharField(
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                default="medium",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="prep_time",
            field=models.IntegerField(
                default=0, help_text="Preparation time in minutes"
            ),
        ),
        migrations.AddField(
            model_name="recipe",
            name="servings",
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name="recipe",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="ingredients",
        ),
        migrations.AlterField(
            model_name="recipe",
            name="name",
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name="RecipeIngredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "unit",
                    models.CharField(
                        choices=[
                            ("g", "Grams"),
                            ("kg", "Kilograms"),
                            ("oz", "Ounces"),
                            ("lb", "Pounds"),
                            ("cup", "Cups"),
                            ("tbsp", "Tablespoons"),
                            ("tsp", "Teaspoons"),
                            ("ml", "Milliliters"),
                            ("l", "Liters"),
                            ("piece", "Pieces"),
                            ("pinch", "Pinch"),
                            ("whole", "Whole"),
                            ("to_taste", "To Taste"),
                        ],
                        max_length=50,
                    ),
                ),
                ("optional", models.BooleanField(default=False)),
                ("notes", models.CharField(blank=True, max_length=200)),
                (
                    "ingredient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.ingredient"
                    ),
                ),
                (
                    "recipe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.recipe"
                    ),
                ),
            ],
            options={
                "ordering": ["recipe", "ingredient"],
            },
        ),
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="api.RecipeIngredient", to="api.ingredient"
            ),
        ),
    ]
