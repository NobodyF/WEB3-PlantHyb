# Generated by Django 5.0.1 on 2024-01-18 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_contactmessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactmessage',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='contactmessage',
            name='sender_name',
            field=models.CharField(max_length=100),
        ),
    ]