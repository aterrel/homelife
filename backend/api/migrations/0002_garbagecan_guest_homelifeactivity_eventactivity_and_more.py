# Generated by Django 5.1.5 on 2025-02-11 12:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GarbageCan",
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
                ("deleted_at", models.DateTimeField(auto_now_add=True)),
                (
                    "deleted_event",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.event",
                    ),
                ),
                (
                    "deleted_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.meal",
                    ),
                ),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="garbage_can",
                        to="api.home",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Guest",
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
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guests",
                        to="api.home",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HomeLifeActivity",
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
                (
                    "action",
                    models.CharField(
                        choices=[
                            ("created", "Created"),
                            ("updated", "Updated"),
                            ("deleted", "Deleted"),
                            ("canceled", "Canceled"),
                        ],
                        max_length=50,
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                ("entity_type", models.CharField(max_length=50)),
                ("entity_id", models.IntegerField()),
                (
                    "home",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activity_logs",
                        to="api.home",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activity_logs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventActivity",
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
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to="api.event",
                    ),
                ),
                (
                    "activity_log",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.homelifeactivity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChoreActivity",
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
                (
                    "chore",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to="api.chore",
                    ),
                ),
                (
                    "activity_log",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.homelifeactivity",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MealActivity",
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
                (
                    "activity_log",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.homelifeactivity",
                    ),
                ),
                (
                    "meal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to="api.meal",
                    ),
                ),
            ],
        ),
    ]
