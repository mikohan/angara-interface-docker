# -*- coding: utf-8 -*-

# from rest_framework_recursive.fields import RecursiveField
from product.models import Cross
from rest_framework import serializers
from product.models import (
    Product,
    ProductImage,
    Category,
    Units,
    CarModel,
    CarMake,
    CarEngine,
    Country,
    BrandsDict,
    ProductVideos,
    Category,
    ProductDescription,
    ProductAttribute,
    ProductAttributeName,
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for all categories in flat mode"""

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "cat_image", "level", "parent")


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)  # type: ignore
        return serializer.data


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    This class give us caregories in tree wiew json for front end
    """

    children = RecursiveField(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children", "slug")


class CategoryFirstLevelSerializer(serializers.ModelSerializer):
    """
    First level Category Serializer
    """

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children", "slug")
        depth = 1


class MpttTestSerializer(serializers.ModelSerializer):
    """
    First level Category Serializer
    """

    # some_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "children", "slug")
        depth = 1

    def get_some_count(self, obj):
        return obj.some_count


class ProductCrossSerializer(serializers.ModelSerializer):
    """
    Serializer for getting product Crosses
    """

    class Meta:
        model = Cross
        fields = ["cross"]
        depth = 0


class GetSingleProductSerializer(serializers.ModelSerializer):
    """
    Serializer for getting single product for site no authentication required
    Also getting all related fields like images, videos, attributes, etc...
    """

    product_cross = ProductCrossSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "name2",
            "cat_number",
            "slug",
            "brand",
            "unit",
            "car_model",
            "category",
            "related",
            "engine",
            "product_image",
            "product_video",
            "product_description",
            "product_cross",
            "product_attribute",
            "one_c_id",
        ]
        depth = 2  # Dont change it All may craches


class GetCarModelSerializer(serializers.ModelSerializer):
    """
    Getting car models required from UI
    """

    class Meta:
        model = CarModel
        fields = "__all__"
        depth = 1


class GetCarMakesSerializer(serializers.ModelSerializer):
    """
    Car Makes All list API
    """

    class Meta:
        model = CarMake
        fields = "__all__"
