# Generated by Django 5.1.7 on 2025-05-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("labels", "0001_initial"),
        ("tasks", "0008_alter_tasks_discription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tasks",
            name="author",
            field=models.TextField(
                blank=True, max_length=150, null=True, verbose_name="Author"
            ),
        ),
        migrations.AlterField(
            model_name="tasks",
            name="label",
            field=models.ManyToManyField(
                blank=True, null=True, to="labels.labels", verbose_name="Labels"
            ),
        ),
    ]
