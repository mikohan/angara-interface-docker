# Generated by Django 3.0.3 on 2020-07-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0043_auto_20200613_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='main',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
