# -*- coding: utf-8 -*-

from users.models import AutoUser
from product.utils import categorizer_split

# from product.utils import categorizer
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
import os
from brands.models import BrandsDict
from product.utils import unique_slug_generator, get_youtube_id
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from PIL import Image as Img
import io
from django.db.models.signals import post_delete
from django.dispatch import receiver
from PIL import Image, ImageOps
from product.utils import delete_file
from mptt.models import MPTTModel, TreeForeignKey
from product.utils import unique_slug_generator
from product.models.models_vehicle import CarModel
from product.models.models_images import ProductImage
from product.models.models_productfields import ProductBages, ProductVideos
import random
from quora.common_lib.logger import logger


class Category(MPTTModel):  # MPTT model here for now

    name = models.CharField(max_length=50, unique=True, db_index=True)
    type = models.CharField(max_length=30, default="shop")
    layout = models.CharField(max_length=30, default="products")
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
        on_delete=models.DO_NOTHING,
    )
    old_group_id = models.IntegerField(blank=True)
    slug = models.SlugField(blank=True)

    plus = models.CharField(max_length=1000, blank=True)
    minus = models.CharField(max_length=1000, blank=True)
    full_plus = models.TextField(null=True, blank=True)
    full_minus = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(
        "CategoryTags", blank=True, related_name="category_tags"
    )
    cat_image = models.ImageField(
        upload_to=settings.CATEGORY_IMAGES, blank=True, null=True
    )
    weight = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        help_text="Вес категории от 0 до 5. Больше вес - выше показывается",
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        unique_together = (
            "parent",
            "slug",
        )
        verbose_name_plural = "Категории"

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append("/".join(ancestors[: i + 1]))
        return slugs

    def __str__(self):
        return self.name

    @property
    def image(self):
        image = None
        if self.cat_image:
            image = settings.SITE_URL + self.cat_image.url
        else:
            image = "http://localhost:8000/media/images/categories/default.jpg"
        return image

    @property
    def items(self):
        return 123


# Product Description
class ProductRating(models.Model):
    class Rating(models.IntegerChoices):
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5

    score = models.IntegerField(
        choices=Rating.choices, null=True, blank=True, default=random.randint(3, 5)
    )
    quantity = models.IntegerField(null=True, blank=True, default=random.randint(1, 20))
    product = models.ForeignKey(
        "product",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="product_rating",
    )
    autoUser = models.ForeignKey(
        AutoUser,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="autouser_rating",
    )

    class Meta:
        unique_together = ("product", "autoUser")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return str(f"{self.product.name} id: {self.product.id}")


class Product(models.Model):  # Main table product

    name = models.CharField(max_length=255, db_index=True)
    name2 = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(
        BrandsDict,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="product_brand",
    )

    car_model = models.ManyToManyField(CarModel, related_name="model_product")
    cat_number = models.CharField(max_length=255, db_index=True)
    oem_number = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    category = TreeManyToManyField(
        Category, related_name="category_reverse", blank=True
    )
    # Field for the cross selling products many many
    related = models.ManyToManyField("self", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True)
    one_c_id = models.IntegerField(blank=True, null=True, unique=True)
    unit = models.ForeignKey(
        "Units",
        on_delete=models.DO_NOTHING,
        related_name="product_unit",
        blank=True,
        null=True,
    )
    condition = models.CharField(max_length=20, null=True, blank=True, default="new")
    active = models.BooleanField(default=True)
    engine = models.ManyToManyField(
        "CarEngine", related_name="car_related_engine", blank=True
    )

    def __str__(self):
        return f"{self.name}-one-c={self.one_c_id}-id={self.id}"  # type: ignore

    @property
    def make_name(self):
        car_make = ""
        car_model = ""
        name2 = self.name2 or ""
        try:
            car_model = self.car_model.first()
            car_make = car_model.carmake
            name = self.name.title()
            # if любая марка или любая модель
            if car_model.id == 26 or car_make.id == 8:
                return f"{name} {name2.title()}"

            return f"{name} для {car_make.name.title()} {car_model.name.title()} {name2.title()}"

        except:
            logger(
                f"{self.name}, {self.one_c_id} \n",
                "fucked_products.log",
                "product_logs",
            )
            return f"{self.name.title()} {name2.title()}"

    @property
    def bages(self):
        if self.product_bages:
            return [x.name for x in self.product_bages.all()]
        else:
            return []

    @property
    def full_name(self):
        if self.name2:
            cars = [x.name for x in self.car_model.all()]
            cars_str = " ".join(cars)
            return self.name + " " + cars_str + " " + self.name2
        else:
            return self.name

    @property
    def description(self):
        try:
            return self.product_description.text
        except:
            return ""

    @property
    def excerpt(self):
        try:
            if self.product_description:
                spl = self.product_description.text.split(".")[:5]
                return (".").join(spl)
        except:
            return ""

    @property
    def sku(self):
        return self.one_c_id

    @property
    def partNumber(self):
        return self.cat_number

    @property
    def images(self):
        return self.product_image.all()  # type: ignore

    @property
    def old_imgs(self):
        return self.old_images.all()  # type: ignore

    """
    Below properties needs to be refactored
    For now it is stub

    """

    @property
    def compareAtPrice(self):
        return self.price + 100

    @property
    def have_photo_in_folder(self):
        working_dir = settings.PHOTO_FOLDER_FOR_CHECK
        for directory in os.listdir(working_dir):
            if str(self.one_c_id) in directory:
                return True

        return False

    @property
    def have_photo(self):
        return self.product_image.exists()

    @property
    def have_attribute(self):
        return self.product_attribute.exists()

    @property
    def have_description(self):
        if not hasattr(self.product_description, "text"):
            return False
        else:
            if len(self.product_description.text) > 0:
                return True
            else:
                return False
        if not self.product_description:
            return False
        return False

    @property
    def have_video(self):
        return self.product_video.exists()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [models.Index(fields=["cat_number", "name", "slug"])]


class AngaraOld(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    car_model = models.IntegerField()
    one_c_id = models.IntegerField()
    cat_number = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class Cross(models.Model):
    cross = models.CharField(max_length=50)
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="product_cross", blank=True
    )

    class Meta:
        verbose_name = "Кросс"
        verbose_name_plural = "Кроссы"

    def __str__(self):
        return self.product.name


################### Category pre save receiver ####################################


def post_save_categorizer(sender, instance, *args, **kwargs):  #

    categorizer_split(instance, Category)


post_save.connect(post_save_categorizer, Product)


################### Slug pre save receiver ####################################


def product_slug_save(sender, instance, *args, **kwargs):  # Slug saver

    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(product_slug_save, Product)

################### CarModel Slug pre save receiver ####################################


def car_slug_save(sender, instance, *args, **kwargs):  # Slug saver

    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(car_slug_save, CarModel)

################### Slug pre save receiver Category ####################################


def category_slug_save(sender, instance, *args, **kwargs):  # Slug saver
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(category_slug_save, Category)

#################### Youtube ID Pre Save Receiver #############################


def youtube_id_save(sender, instance, *args, **kwargs):  # youtube id saver
    instance.youtube_id = get_youtube_id(instance.url)


pre_save.connect(youtube_id_save, ProductVideos)


#################### File Delete Post Delete Receiver #########################


def delete_files(sender, instance, *args, **kwargs):
    if instance.image:
        delete_file(instance.image.path)
    if instance.img150:
        delete_file(instance.img150.path)
    if instance.img245:
        delete_file(instance.img245.path)
    if instance.img500:
        delete_file(instance.img500.path)
    if instance.img800:
        delete_file(instance.img800.path)


post_delete.connect(delete_files, ProductImage)
