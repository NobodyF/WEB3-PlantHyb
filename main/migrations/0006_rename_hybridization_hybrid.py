# Generated by Django 5.0.1 on 2024-01-17 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_plant_name_hybridization'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Hybridization',
            new_name='Hybrid',
        ),
    ]
