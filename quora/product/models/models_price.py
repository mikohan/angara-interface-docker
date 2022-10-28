from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from product.models.models import Product


def get_default_store():
    try:
        store = Store.objects.get(id=3)
        return store
    except:
        print("No store in the database")
    return None


class Store(models.Model):
    """
    Class for handling stores
    """

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    location_city = models.CharField(max_length=50)
    location_address = models.CharField(max_length=100)


# Probably need to delete
class Price(models.Model):
    """
    Class handling product prices
    """

    product = models.OneToOneField(
        "Product", on_delete=models.CASCADE, related_name="product_prices"
    )

    retail_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True, default=None
    )
    purchase_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True, default=None
    )

    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"

    def __str__(self):
        return self.product.full_name


class PriceHistory(models.Model):
    """
    Class handling product price history
    Needs to implement logic and add it ot crontab later on
    """

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"

    def __str__(self):
        return self.product.full_name

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_price_history"
    )
    retail_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True, default=None
    )
    purchase_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True, default=None
    )
    dollar_rate = models.FloatField()
    date = models.DateField(auto_now_add=True)


class Stock(models.Model):
    """
    Handling products on stock
    """

    class Meta:
        verbose_name = "Сток"
        verbose_name_plural = "Стоки"
        unique_together = ("product", "store")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_stock"
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="store_stock",
        default=1,
    )
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    availability_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product.full_name
