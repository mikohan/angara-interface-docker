# Generated by Django 3.0.2 on 2022-11-17 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0116_auto_20221117_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productrating',
            name='quantity',
            field=models.IntegerField(blank=True, default=3, null=True),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='score',
            field=models.IntegerField(blank=True, choices=[(1, 'One Star'), (2, 'Two Stars'), (3, 'Three Stars'), (4, 'Four Stars'), (5, 'Five Stars')], default=5, null=True),
        ),
    ]
