# Generated by Django 3.0.2 on 2021-07-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0090_auto_20210711_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='model_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='model_liquids',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='model_to',
            field=models.TextField(blank=True, null=True),
        ),
    ]
