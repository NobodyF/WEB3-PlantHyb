# Generated by Django 5.0.1 on 2024-06-09 12:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_plant_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='HybridTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('hybrid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='main.hybrid')),
            ],
        ),
    ]
