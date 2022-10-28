from django.db import models

from django.db.models.signals import pre_save
from product.utils import unique_slug_generator
from test_category.api.helpers.description_text import desc
from random import randrange


# Create your models here.
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField, TreeManager


class Brands(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="test_category", blank=True)
    country = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    categories = models.ManyToManyField(
        "Categories", related_name="reverse_categories")
    brand = models.ForeignKey(Brands, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField()
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "Товар"

    def __str__(self):
        return self.name

    @property
    def compareAtPrice(self):
        return self.price + self.price * 0.2

    # @property
    # def price(self):
    #     return 123

    @property
    def stock(self):
        return "in-stock"

    @property
    def sku(self):
        return "14567"

    @property
    def partNumber(self):
        return "346005F000"

    @property
    def description(self):
        return desc()

    @property
    def excerpt(self):
        return "Описание товара после заголовка в карточке товара на сайте."

    @property
    def availability(self):
        return "in-stock"

    @property
    def tags(self):
        return ["Brake Kit", "Brandix", "Filter", "Bumper", "Transmission", "Hood"]

    @property
    def type(self):
        return {
            "slug": "default",
            "name": "Default",
            "attributeGroups": [
                {
                    "name": "General",
                    "slug": "general",
                    "attributes": [
                        "speed",
                        "power-source",
                        "battery-cell-type",
                        "voltage",
                        "battery-capacity",
                        "material",
                        "engine-type",
                    ],
                },
                {
                    "name": "Dimensions",
                    "slug": "dimensions",
                    "attributes": ["length", "width", "height"],
                },
            ],
        }

    @property
    def attributes(self):
        return [
            {
                "name": "Speed",
                "slug": "speed",
                "featured": "true",
                "values": [{"name": "750 RPM", "slug": "750-rpm"}],
            },
            {
                "name": "Power Source",
                "slug": "power-source",
                "featured": "true",
                "values": [{"name": "Cordless-Electric", "slug": "cordless-electric"}],
            },
            {
                "name": "Battery Cell Type",
                "slug": "battery-cell type",
                "featured": "true",
                "values": [{"name": "Lithium", "slug": "lithium"}],
            },
            {
                "name": "Voltage",
                "slug": "voltage",
                "featured": "true",
                "values": [{"name": "20 Volts", "slug": "20-volts"}],
            },
            {
                "name": "Battery Capacity",
                "slug": "battery-capacity",
                "featured": "true",
                "values": [{"name": "2 Ah", "slug": "2-ah"}],
            },
            {
                "name": "Material",
                "slug": "material",
                "featured": "false",
                "values": [
                    {"name": "Aluminium", "slug": "aluminium"},
                    {"name": "Plastic", "slug": "plastic"},
                ],
            },
            {
                "name": "Engine Type",
                "slug": "engine-type",
                "featured": "false",
                "values": [{"name": "Brushless", "slug": "brushless"}],
            },
            {
                "name": "Length",
                "slug": "length",
                "featured": "false",
                "values": [{"name": "99 mm", "slug": "99-mm"}],
            },
            {
                "name": "Width",
                "slug": "width",
                "featured": "false",
                "values": [{"name": "207 mm", "slug": "207-mm"}],
            },
            {
                "name": "Height",
                "slug": "height",
                "featured": "false",
                "values": [{"name": "208 mm", "slug": "208-mm"}],
            },
            {
                "name": "Color",
                "slug": "color",
                "featured": "false",
                "values": [{"name": "White", "slug": "white"}],
            },
        ]

    @property
    def options(self):
        return [
            {
                "type": "default",
                "slug": "material",
                "name": "Material",
                "values": [
                    {"slug": "steel", "name": "Steel"},
                    {"slug": "aluminium", "name": "Aluminium"},
                    {"slug": "thorium", "name": "Thorium"},
                ],
            },
            {
                "type": "color",
                "slug": "color",
                "name": "Color",
                "values": [
                    {"slug": "white", "name": "White", "color": "#fff"},
                    {"slug": "yellow", "name": "Yellow", "color": "#ffd333"},
                    {"slug": "red", "name": "Red", "color": "#ff4040"},
                    {"slug": "blue", "name": "Blue", "color": "#4080ff"},
                ],
            },
        ]

    @property
    def images(self):
        return [
            "http://localhost:8000/media/123/555_tf/IMG_4210.jpg",
            "http://localhost:8000/media/123/555_tf/IMG_4213.jpg",
            "http://localhost:8000/media/123/555_tf/IMG_4281.jpg",
            "http://localhost:8000/media/123/555_tf/IMG_4288.JPG",
        ]

    @property
    def badges(self):
        return ["sale", "new", "hot"]

    @property
    def compatibility(self):
        return [1, 2]

    # @property
    # def rating(self):
    #     return randrange(2, 5, 1)

    @property
    def reviews(self):
        return 7


class CategoryManager(TreeManager):
    def get_queryset(self):
        return (
            # super().get_queryset()
            # .annotate(count=models.Count("reverse_categories"))
            super().add_related_count(
                super().get_queryset(), Product, "categories", "count", cumulative=True
            )
        )


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
    slug = models.SlugField(blank=True)

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

    # @property
    # def layout(self):
    #     return "products"


"""
Pre save slug generators starts
"""


def brand_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, instance.name, instance.slug)


pre_save.connect(brand_slug, Brands)


def product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, instance.name, instance.slug)


pre_save.connect(product_slug, Product)


def category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(
            instance, instance.name, instance.slug)


pre_save.connect(category_slug, Categories)


# Pre save Product fields logics


def product_price(sender, instance, *args, **kwargs):
    if not instance.price:
        instance.price = randrange(5, 100, 5)


pre_save.connect(product_price, Product)
