# Generated by Django 5.0.1 on 2024-05-09 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_hybrid_anthocyanin_coloration_degree_of_fruit_abscission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=100)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.plant')),
            ],
        ),
    ]