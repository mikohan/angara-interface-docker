# Generated by Django 3.0.2 on 2022-11-12 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0114_auto_20221112_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='quantity',
            field=models.IntegerField(blank=True, default=14, null=True),
        ),
    ]
