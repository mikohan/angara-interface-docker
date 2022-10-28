from django.db import models
from users.models import CustomUser
from django.db.models.signals import pre_save
from product.utils import unique_slug_generator


class Makes(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Марка"

    def __str__(self):
        return self.name


class Years(models.Model):
    year = models.IntegerField()

    class Meta:
        verbose_name = "Год"

    def __str__(self):
        return f"{self.year}"


class Vehicle(models.Model):

    slug = models.SlugField(blank=True, null=True)

    year_from = models.ForeignKey(
        Years, on_delete=models.DO_NOTHING, related_name="year_from"
    )
    year_to = models.ForeignKey(
        Years, on_delete=models.DO_NOTHING, related_name="year_to"
    )
    make = models.ForeignKey(Makes, on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=255)
    engine = models.ForeignKey("Engine", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Автомобил"
        verbose_name_plural = "Автомобили"

    @property
    def year(self):
        return [int(self.year_from.year), int(self.year_to.year)]

    def __str__(self):
        return self.model


class Country(models.Model):
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class Engine(models.Model):

    FUELS = (("D", "Desel"), ("G", "Gasoline"))
    VOLUMES = (
        ("3", "3.0"),
        ("3.5", "3.5"),
        ("2.5", "2.5"),
        ("2", "2.0"),
        ("1.5", "1.5"),
    )

    name = models.CharField(max_length=100)
    fuel = models.CharField(max_length=10, choices=FUELS, default="D")
    volume = models.CharField(max_length=10, choices=VOLUMES, default="2.5")
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = "Двигатель"

    def __str__(self):
        return self.name


class UserVehicles(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user")
    vehicles = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="vehicles"
    )

    class Meta:

        verbose_name = "Машина Пользователя"
        verbose_name_plural = "Машины пользователя"

    def __str__(self):
        return self.user.username


##
# Pre save vehicle slug fields logics


def vehicle_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.model, instance.slug)


pre_save.connect(vehicle_slug, Vehicle)


# presave slug for makes


def makes_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(makes_slug, Makes)


# presave slug for Contries


def countries_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(countries_slug, Country)
