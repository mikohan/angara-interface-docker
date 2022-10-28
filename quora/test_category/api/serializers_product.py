from rest_framework import serializers
from .serializers import CategoriesSerializer
from test_category.models import Product, Brands


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ["id", "name", "slug", "image", "country"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for getting single product for site no authentication required
    Also getting all related fields like images, videos, attributes, etc...
    """

    # attributes = AttributesSerializer(many=True, read_only=True)
    # images = ProductImagesSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    categories = CategoriesSerializer(many=True, read_only=True)  # , source="category")

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "categories",
            "brand",
            # "images",
            # "excerpt",
            # "description",
            # "slug",
            # "sku",
            # "partNumber",
            # "stock",
            # "price",
            # "compareAtPrice",
            # "badges",
            # "rating",
            # "reviews",
            # "availability",
            # "compatibility",
            # "type",
            # "attributes",
            # "options",
            # "tags",
        ]
        depth = 0  # Dont change it All may craches
