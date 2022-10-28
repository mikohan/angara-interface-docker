from django.db import models

from django.utils.text import slugify
from transliterate import translit


class ProductBages(models.Model):
    class BagesChoices(models.TextChoices):
        SALE = ("SALE", "РАСПРОДАЖА")
        NEW = ("NEW", "НОВИНКА")

    name = models.CharField(
        max_length=20, null=True, blank=True, choices=BagesChoices.choices
    )
    product = models.ForeignKey(
        "Product",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="product_bages",
    )

    class Meta:
        unique_together = ("name", "product")
        verbose_name = "Бейдж"
        verbose_name_plural = "Бейджи"

    def __str__(self):
        return self.name


class CategoryTags(models.Model):
    name = models.CharField(max_length=50)


class Units(models.Model):  # Units for parts
    unit_name = models.CharField(max_length=10, default="шт")

    class Meta:
        verbose_name = "Еденица измерения"
        verbose_name_plural = "Еденицы измерения"

    def __str__(self):
        return self.unit_name


# Product Videos
class ProductVideos(models.Model):
    youtube_id = models.CharField(max_length=45, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_video",
    )

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class ProductDescription(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    product = models.OneToOneField(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_description",
    )

    class Meta:
        verbose_name = "Описание товара"
        verbose_name_plural = "Описания товара"


# Crosses parts


class ProductAttributeName(models.Model):
    """
    Класс содержит названия атрибутов.
    При создании нового атрибута будет проверятся если он есть,
    то просто добавляем значение.
    Если нет, то создаем новое название атрибута и сохраняем значение в модели
    ProductAttribute
    """

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Название Атрибута"
        verbose_name_plural = "Названия Атрибутов"

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    This model has to manage attributes.
    It has to be devided by two classes.
    One class for attribute names.
    Another one for attributes values.
    And it has to be connected to Product model.
    """

    attribute_name = models.ForeignKey(
        ProductAttributeName, on_delete=models.CASCADE, related_name="atr_name"
    )
    attribute_value = models.CharField(
        max_length=45, null=True, verbose_name="Значение атрибута"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Относится к Товару",
        related_name="product_attribute",
    )

    class Meta:
        verbose_name = "Атрибут"
        verbose_name_plural = "Атрибуты"

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(translit(self.attribute_name, "ru", reverse=True))

    def __str__(self):
        return self.attribute_value
