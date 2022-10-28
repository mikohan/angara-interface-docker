from rest_framework import serializers
from product.models import Product


class ItemSerializer(serializers.Serializer):
    type = serializers.CharField()
    count = serializers.CharField()
    updatedAt = serializers.DateTimeField()


class SkuSerializer(serializers.Serializer):
    sku = serializers.CharField()
    warehouseId = serializers.CharField()
    items = ItemSerializer(many=True)


class GetStockSerializer(serializers.Serializer):
    skus = SkuSerializer(many=True)
