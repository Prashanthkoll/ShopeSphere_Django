# Generated by Django 5.1.6 on 2025-03-06 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.IntegerField(default='_I@IntegerField'),
        ),
    ]
