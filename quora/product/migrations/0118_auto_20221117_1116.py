# Generated by Django 3.0.2 on 2022-11-17 08:16

from django.db import migrations, models
import product.models.models_images


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0117_auto_20221117_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='oldproductimage',
            name='image150_webp',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.models_images.img_path_old),
        ),
        migrations.AddField(
            model_name='oldproductimage',
            name='image245_webp',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.models_images.img_path_old),
        ),
        migrations.AddField(
            model_name='oldproductimage',
            name='image500_webp',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.models_images.img_path_old),
        ),
        migrations.AddField(
            model_name='oldproductimage',
            name='image800_webp',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.models_images.img_path_old),
        ),
        migrations.AddField(
            model_name='oldproductimage',
            name='image_webp',
            field=models.ImageField(blank=True, null=True, upload_to=product.models.models_images.img_path_old),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='quantity',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
        migrations.AlterField(
            model_name='productrating',
            name='score',
            field=models.IntegerField(blank=True, choices=[(1, 'One Star'), (2, 'Two Stars'), (3, 'Three Stars'), (4, 'Four Stars'), (5, 'Five Stars')], default=4, null=True),
        ),
    ]