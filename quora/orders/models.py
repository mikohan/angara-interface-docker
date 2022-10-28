from users.models import AutoUser, CustomUser
from django.db import models
from product.models import Product
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver


class Orders(models.Model):
    class StatusChoices(models.TextChoices):
        ORDERED = ("ORD", "ПОЛУЧЕН")
        INPROGRESS = ("PROG", "СОБИРАЕТСЯ")
        SENT = ("SENT", "ОТПРАВЛЕН")
        DELIVERED = ("DELIV", "ДОСТАВЛЕН")

    class PaymentChoices(models.TextChoices):
        ONGET = ("onGet", "ПРИ ПОЛУЧЕНИИ")
        ONSITE = ("onLine", "ОНЛАЙН")

    class DeliveryChoices(models.TextChoices):
        SELF = ("self", "САМОВЫВОЗ")
        KUR = ("kur", "КУРЬЕРОМ")
        POST = ("post", "ТРАНСПОРТНОЙ КОМПАНИЕЙ")

    date = models.DateTimeField(auto_now_add=True)
    number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50, choices=StatusChoices.choices, default=StatusChoices.ORDERED
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    autouser = models.ForeignKey(
        AutoUser, on_delete=models.CASCADE, null=True, blank=True
    )
    payment = models.CharField(
        max_length=50, choices=PaymentChoices.choices, default=PaymentChoices.ONGET
    )
    delivery = models.CharField(
        max_length=50, choices=DeliveryChoices.choices, default=DeliveryChoices.SELF
    )
    total_front = models.DecimalField(
        max_digits=14, decimal_places=2, null=True, blank=True
    )
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.number

    @property
    def total(self):
        sum = 0
        try:
            prods = self.order_products.all()
            for prod in prods:
                sum += float(prod.product_price)
        except:
            pass
        print(sum)
        return sum


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name="order_products"
    )
    product_id = models.IntegerField()
    product_price = models.DecimalField(max_digits=14, decimal_places=2)
    product_name = models.CharField(max_length=555)
    product_car = models.CharField(max_length=255)
    product_brand = models.CharField(max_length=255)
    product_one_c_id = models.CharField(max_length=40, null=True, blank=True)
    product_cat_number = models.CharField(max_length=40, null=True, blank=True)
    product_image = models.CharField(max_length=500, blank=True, null=True)
    product_slug = models.SlugField(max_length=500)
    qty = models.IntegerField()
    image = models.CharField(max_length=555, null=True, blank=True)

    class Meta:
        verbose_name = "Детали заказа"
        verbose_name_plural = "Детали заказа"

    def __str__(self):
        return self.product_name
