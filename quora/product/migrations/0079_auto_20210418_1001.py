# Generated by Django 3.0.2 on 2021-04-18 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0078_product_ratingquantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='product',
            name='ratingQuantity',
        ),
        migrations.AddField(
            model_name='productrating',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_rating', to='product.Product'),
        ),
    ]
