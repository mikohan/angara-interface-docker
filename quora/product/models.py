# -*- coding: utf-8 -*-

from product.utils import categorizer_split

# from product.utils import categorizer
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
import os
from brands.models import BrandsDict
from product.utils import unique_slug_generator, get_youtube_id
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
import io
from django.db.models.signals import post_delete
from django.dispatch import receiver
from PIL import Image, ImageOps
from product.utils import delete_file
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    name = models.CharField(max_length=100)
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
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        verbose_name = "Категории"

    def __str__(self):
        return self.name + "-" + str(self.level)

    # objects = CategoryManager()

    @property
    def image(self):
        return "http://localhost:8000/media/123/555_tf/IMG_4210.jpg"

    # @property
    # def type(self):
    #     return "shop"

    @property
    def items(self):
        return 123


class Category(MPTTModel):  # MPTT model here for now
    name = models.CharField(max_length=50, unique=True)
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
    slug = models.SlugField(blank=True, unique=True)

    plus = models.CharField(max_length=1000, blank=True)
    minus = models.CharField(max_length=1000, blank=True)
    full_plus = models.TextField(null=True, blank=True)
    full_minus = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(
        "CategoryTags", blank=True, related_name="category_tags"
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
        return "http://localhost:8000/media/123/555_tf/IMG_4210.jpg"

    @property
    def items(self):
        return 123


class CategoryTags(models.Model):
    name = models.CharField(max_length=50)


class Units(models.Model):  # Units for parts
    unit_name = models.CharField(max_length=10, default="шт")

    class Meta:
        verbose_name = "Еденица измерения"
        verbose_name_plural = "Еденицы измерения"

    def __str__(self):
        return self.unit_name


# Class Country
class Country(models.Model):
    country = models.CharField(max_length=45)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.country


# Car Make class
class CarMake(models.Model):
    name = models.CharField(max_length=45)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        verbose_name = "Марка Машины"
        verbose_name_plural = "Марки Машин"

    def __str__(self):
        return self.name


class CarEngine(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        verbose_name = "Двигатель"
        verbose_name_plural = "Двигатели"

    def __str__(self):
        return self.name


# Car Model class


class CarModel(models.Model):
    name = models.CharField(max_length=45, blank=True)
    engine = models.ManyToManyField(CarEngine, blank=True, related_name="car_engine")
    carmake = models.ForeignKey(
        CarMake, on_delete=models.DO_NOTHING, related_name="car_model"
    )
    slug = models.CharField(max_length=45, blank=True)

    class Meta:
        verbose_name = "Модель Машины"
        verbose_name_plural = "Модели Машины"

    def __str__(self):
        return self.name


# Custom path to upload images
def img_path(instance, filename, *args, **kwargs):
    path = os.path.join(
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        filename,
    )
    return path


def img_path_tmb(instance, filename, *args, **kwargs):
    path = os.path.join(
        str(instance.product.cat_number),
        str(instance.product.brand).replace(" ", "_"),
        "tmb",
        filename,
    )
    return path


###############################################################################
# Product images
class ProductImage(models.Model):
    image = models.ImageField(max_length=255, upload_to=img_path, null=True, blank=True)
    img150 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img245 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img500 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img800 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img245x245 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img150x150 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img500x500 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    img800x800 = models.ImageField(
        max_length=255, upload_to=img_path_tmb, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    main = models.BooleanField(default=False, blank=True)
    product = models.ForeignKey(
        "Product",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="product_image",
    )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def save(self, *args, **kwargs):

        size = ((150, 100), (245, 164), (500, 333), (900, 600), (1280, 860))
        method = Image.ANTIALIAS

        im = Image.open(io.BytesIO(self.image.read()))
        # im = Image.open(self.image)
        imw, imh = im.size
        if imw > 1920:
            img_big = ImageOps.fit(
                im, (1920, 1280), method=method, bleed=0.0, centering=(0.5, 0.5)
            )
            output = io.BytesIO()
            img_big.save(output, format="JPEG", quality=90)
            output.seek(0)
            self.image = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{self.image.name}",
                "image/jpeg",
                output.getbuffer().nbytes,
                "utf-8",
                None,
            )

        # Rectangle 150x100
        img150 = ImageOps.fit(
            im, size[0], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img150.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img150 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 150x150
        img150x150 = ImageOps.fit(
            im, (150, 150), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img150x150.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img150x150 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 245x164
        img245 = ImageOps.fit(
            im, size[1], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img245.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img245 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 245x245
        img245x245 = ImageOps.fit(
            im, (245, 245), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img245x245.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img245x245 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 500x333
        img500 = ImageOps.fit(
            im, size[2], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img500.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img500 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 500x500
        img500x500 = ImageOps.fit(
            im, (500, 500), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img500x500.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img500x500 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Rectangle 900x600
        img800 = ImageOps.fit(
            im, size[3], method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img800.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img800 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )

        # Square 900x900
        img800x800 = ImageOps.fit(
            im, (900, 900), method=method, bleed=0.0, centering=(0.5, 0.5)
        )
        output = io.BytesIO()
        img800x800.save(output, format="JPEG", quality=90)
        output.seek(0)

        self.img800x800 = InMemoryUploadedFile(
            output,
            "ImageField",
            f"{self.image.name}",
            "image/jpeg",
            output.getbuffer().nbytes,
            "utf-8",
            None,
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.product.slug) + "_" + str(self.id)


###############################################################################


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


# Product Description


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


class Product(models.Model):  # Main table product
    name = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(
        BrandsDict,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="product_brand",
    )
    car_model = models.ManyToManyField(CarModel, related_name="model_product")
    cat_number = models.CharField(max_length=255)
    category = TreeManyToManyField(
        Category, related_name="category_reverse", blank=True
    )
    # Field for the cross selling products many many
    related = models.ManyToManyField("self", blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, blank=True)
    one_c_id = models.IntegerField(blank=True, null=True)
    unit = models.ForeignKey(
        "Units", on_delete=models.DO_NOTHING, related_name="product_unit"
    )
    active = models.BooleanField(default=True)
    engine = models.ManyToManyField(
        "CarEngine", related_name="car_related_engine", blank=True
    )

    @property
    def full_name(self):
        if self.name2:
            return self.name + " " + self.name2
        else:
            return self.name

    @property
    def excerpt(self):
        if self.product_description:
            return "Here is going short description for product"

    # @property
    # def description(self):
    #     return self.product_description.text

    @property
    def sku(self):
        return self.one_c_id

    @property
    def partNumber(self):
        return self.cat_number

    @property
    def images(self):
        return self.product_image.all()

    """
    Below properties needs to be refactored
    For now it is stub

    """

    @property
    def price(self):
        return 199

    @property
    def compareAtPrice(self):
        return self.price + 100

    @property
    def stock(self):
        return "in-stock"

    @property
    def badges(self):
        return ["sale", "new", "hot"]

    @property
    def rating(self):
        return 4

    @property
    def reviews(self):
        return 14

    @property
    def availability(self):
        return "in-stock"

    @property
    def compatibility(self):
        return "all"

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

    def __str__(self):
        return self.name


class AngaraOld(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    car_model = models.IntegerField()
    one_c_id = models.IntegerField()
    cat_number = models.CharField(max_length=45)

    def __str__(self):
        return self.name


# Crosses parts


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

    def __str__(self):
        return self.attribute_value


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
