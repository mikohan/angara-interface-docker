from django.utils.text import slugify
from transliterate import translit
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Class Country
class Country(models.Model):
    country = models.CharField(max_length=45)
    image = models.ImageField(upload_to=settings.CAR_IMAGES, blank=True, null=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.country


# Car Make class
class CarMake(models.Model):
    class Priority(models.IntegerChoices):
        HIGEST = 5, "Higest"
        HIGH = 4, "High"
        MEDUM = 3, "Medium"
        LOW = 2, "Low"
        LOWEST = 1, "Lowest"

    name = models.CharField(max_length=45)
    rusname = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True)
    priority = models.IntegerField(
        choices=Priority.choices, default=Priority.LOWEST, null=True, blank=True
    )
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to=settings.CAR_IMAGES, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, "ru", reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Марка Машины"
        verbose_name_plural = "Марки Машин"

    def __str__(self):
        return self.name


class CarEngine(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    slug = models.SlugField(
        unique=True,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to=settings.CAR_IMAGES, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, "ru", reversed=True))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Двигатель"
        verbose_name_plural = "Двигатели"

    def __str__(self):
        return self.name


# Car Model class


class Years(models.Model):
    year = models.IntegerField()

    class Meta:
        verbose_name = "Год"
        verbose_name_plural = "Годы"

    def __str__(self):
        return f"{self.year}"


class CarModel(models.Model):
    class Priority(models.IntegerChoices):
        HIGEST = 5, "Higest"
        HIGH = 4, "High"
        MEDUM = 3, "Medium"
        LOW = 2, "Low"
        LOWEST = 1, "Lowest"

    name = models.CharField(max_length=45, blank=True, unique=True)
    rusname = models.CharField(max_length=50, blank=True, null=True)
    engine = models.ManyToManyField(CarEngine, blank=True, related_name="car_engine")
    carmake = models.ForeignKey(
        CarMake, on_delete=models.DO_NOTHING, related_name="car_model"
    )
    slug = models.CharField(max_length=45, blank=True)
    priority = models.IntegerField(
        choices=Priority.choices, default=Priority.LOWEST, null=True, blank=True
    )
    weight = models.IntegerField(default=0, null=True, blank=True)

    year_from = models.ForeignKey(
        Years,
        on_delete=models.DO_NOTHING,
        related_name="year_from",
        null=True,
        blank=True,
    )
    year_to = models.ForeignKey(
        Years,
        on_delete=models.DO_NOTHING,
        related_name="year_to",
        null=True,
        blank=True,
    )
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=settings.CAR_IMAGES, blank=True, null=True)
    model_history = models.TextField(null=True, blank=True)
    model_liquids = models.TextField(null=True, blank=True)
    model_to = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Модель Машины"
        verbose_name_plural = "Модели Машины"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.name, "ru", reversed=True))
        super().save(*args, **kwargs)

    @property
    def year(self):
        return [int(self.year_from.year), int(self.year_to.year)]

    def __str__(self):
        return self.name
