# Generated by Django 3.0.2 on 2020-11-26 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0020_vehicle_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='engine',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='makes',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
