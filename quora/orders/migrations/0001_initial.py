# Generated by Django 3.0.2 on 2021-05-27 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0017_delete_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('number', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('ORD', 'ПОЛУЧЕН'), ('PROG', 'СОБИРАЕТСЯ'), ('SENT', 'ОТПРАВЛЕН'), ('DELIV', 'ДОСТАВЛЕН')], default='ORD', max_length=50)),
                ('total', models.DecimalField(decimal_places=2, max_digits=14)),
                ('autouser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.AutoUser')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=14)),
                ('product_name', models.CharField(max_length=555)),
                ('product_car', models.CharField(max_length=255)),
                ('product_brand', models.CharField(max_length=255)),
                ('qty', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Orders')),
            ],
            options={
                'verbose_name': 'Детали заказа',
                'verbose_name_plural': 'Детали заказа',
            },
        ),
    ]
