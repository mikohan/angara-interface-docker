from django.db import models
from product.models import Category


class CategoryYandexMarket(models.Model):
    shop_cat = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="yandex_category"
    )
    cat_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Категория Яндекс"
        verbose_name_plural = "Категории Яндекс"

    def __str__(self):
        return self.name


class CategoryOzon(models.Model):
    shop_cat = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="ozon_category"
    )
    cat_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    ozon_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Категория Ozon"
        verbose_name_plural = "Категории Ozon"

    def __str__(self):
        return self.name
