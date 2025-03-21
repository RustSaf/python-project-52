# Generated by Django 5.1.7 on 2025-03-19 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
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
                ("first_name", models.CharField(max_length=25, verbose_name="Name")),
                ("last_name", models.CharField(max_length=25, verbose_name="Surname")),
                (
                    "username",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Username"
                    ),
                ),
                ("password", models.CharField(max_length=20, verbose_name="Password")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Creation date"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Update date"),
                ),
            ],
        ),
    ]
