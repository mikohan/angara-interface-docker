# Generated by Django 3.0.2 on 2020-03-24 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_auto_20200323_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carengine',
            options={'verbose_name': 'Двигатель', 'verbose_name_plural': 'Двигатели'},
        ),
        migrations.AlterModelOptions(
            name='carmake',
            options={'verbose_name': 'Марка Машины', 'verbose_name_plural': 'Марки Машин'},
        ),
        migrations.AlterModelOptions(
            name='carmodel',
            options={'verbose_name': 'Модель Машины', 'verbose_name_plural': 'Модели Машины'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='cross',
            options={'verbose_name': 'Кросс', 'verbose_name_plural': 'Кроссы'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'verbose_name': 'Атрибут', 'verbose_name_plural': 'Атрибуты'},
        ),
        migrations.AlterModelOptions(
            name='productdescription',
            options={'verbose_name': 'Описание товара', 'verbose_name_plural': 'Описания товара'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
        migrations.AlterModelOptions(
            name='productvideos',
            options={'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AlterModelOptions(
            name='units',
            options={'verbose_name': 'Еденица измерения', 'verbose_name_plural': 'Еденицы измерения'},
        ),
        migrations.AlterField(
            model_name='carengine',
            name='name',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.CarModel'),
        ),
        migrations.AlterField(
            model_name='product',
            name='engine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='product.CarEngine'),
        ),
    ]
