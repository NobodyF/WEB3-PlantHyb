# Generated by Django 5.0.1 on 2024-01-16 11:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Plant",
            fields=[
                (
                    "id",
                    models.CharField(max_length=100, primary_key=True, serialize=False),
                ),
                ("genes", models.CharField(max_length=100)),
            ],
        ),
    ]
