# -*- coding: utf-8 -*-
import random
from django.db.models import Q

from rest_framework_recursive.fields import RecursiveField
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
    ProductRating,
)
from django.conf import settings
from bs4 import BeautifulSoup


class ProductAttribureNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeName
        fields = ["id", "name"]


class ProductAttributeSerializer(serializers.ModelSerializer):

    # attribute_name = ProductAttribureNameSerializer(
    #    instance=ProductAttributeName, read_only=True)

    attribute_text_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttribute
        fields = [
            "id",
            "attribute_text_name",
            "attribute_name",
            "attribute_value",
            "product",
        ]

    def get_attribute_text_name(self, obj):
        return obj.attribute_name.name

    # def create(self, validated_data):

    #     attribute_name_data = validated_data.pop('attribute_name')

    #     try:
    #         attr_name = ProductAttributeName.objects.get(
    #             name=attribute_name_data['name'])
    #     except:
    #         attr_name = ProductAttributeName.objects.create(
    #             name=attribute_name_data['name'])
    #     attr = ProductAttribute.objects.create(
    #         attribute_name=attr_name,
    #         attribute_value=validated_data.get('attribute_value'),
    #         product=Product.objects.get(id=validated_data.get('product').id)
    #     )
    #     return attr


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    """
    Image serialization class
    Later needs to implement main image logic
    It defenantly needs to be made rectangle shape
    """

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "product",
            "img150",
            "img245",
            "img500",
            "img800",
            "main",
        ]


###############################################################################
############### IMPLEMENT WHEN ARRIVE #########################################
###############################################################################

# def update(self, instance, validated_data):
#     img_mapping = {img.id: img for img in instance}
#     data_mapping = {item['id']: item for item in validated_data}
#     print('Instance', data_mapping, data_mapping)
#     # for obj in instance:
#     #     print(obj.)
#     # instance.main = validated_data.get('main', instance.main)


#     # instance.save()
#     return instance


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideos
        fields = ["id", "url", "product", "youtube_id"]


class UnitsSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Units()._meta.get_field("id"))

    class Meta:
        model = Units
        fields = ("id", "unit_name")


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class CarMakeSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = CarMake
        fields = "__all__"


class CarModelSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=CarModel()._meta.get_field("id"))

    carmake = CarMakeSerializer(instance=CarMake, required=False, read_only=True)

    class Meta:
        model = CarModel
        fields = ["id", "carmake", "name"]


class CarEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarEngine
        fields = "__all__"


class CarEngineSerializerSession(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=CarEngine()._meta.get_field('id'))

    class Meta:
        model = CarEngine
        fields = "__all__"


class CarModelSerializerSession(serializers.ModelSerializer):
    # id = serializers.ModelField(model_field=CarModel()._meta.get_field('id'))

    class Meta:
        model = CarModel
        fields = "__all__"  # ['id', 'name']


class SessionSerializer(serializers.Serializer):
    car_model = CarModelSerializerSession(
        instance=CarModel
    )  # serializers.IntegerField()
    car_engine = CarEngineSerializerSession(
        instance=CarEngine
    )  # serializers.IntegerField()

    class Meta:
        fields = "__all__"


class BrandsDictSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=BrandsDict()._meta.get_field("id"))

    class Meta:
        model = BrandsDict
        fields = ("id", "brand")


class ProductRelatedSerializer(serializers.ModelSerializer):

    """
    This Serializer made for adding related product only for product instance
    """

    class Meta:
        model = Product
        fields = ["id", "related"]


class CrossSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = Cross
        fields = ["id", "cross"]


class ProductSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=True, required=False)
    product_cross = CrossSerializer(many=True, required=False)

    class Meta:
        model = Product
        # fields = '__all__'
        fields = [
            "id",
            "name",
            "name2",
            "cat_number",
            "oem_number",
            "category",
            "slug",
            "brand",
            "car_model",
            "unit",
            "one_c_id",
            "active",
            "engine",
            "product_cross",
        ]

        # represent full fields of serializer nested objects
        depth = 0

    # Create method
    def create(self, validated_data):
        # car models array
        car_model_data = validated_data.pop("car_model")
        car_model_list = [x.id for x in car_model_data]
        car_model_qs = CarModel.objects.filter(id__in=car_model_list)
        # engines array
        car_engine_data = validated_data.pop("engine")
        car_engine_list = [x.id for x in car_engine_data]
        car_engine_qs = CarEngine.objects.filter(id__in=car_engine_list)

        brand_qs = BrandsDict.objects.get(id=validated_data.get("brand").id)
        unit_qs = Units.objects.get(id=validated_data["unit"].id)

        product = Product.objects.create(
            name=validated_data["name"],
            name2=validated_data["name2"],
            cat_number=validated_data["cat_number"],
            # Here is some point to check in future on card it is no field oem number
            oem_number=validated_data["cat_number"],
            # oem_number=validated_data["oem_number"],
            brand=brand_qs,
            # car_model=car_model_qs,
            unit=unit_qs,
            one_c_id=validated_data["one_c_id"],
            active=validated_data["active"],
        )

        product.save()
        # Tryed save
        # rating = ProductRating(
        #     product=product, score=random.randint(3, 5), quantity=random.randint(1, 20)
        # )
        # rating.save()
        for engine in car_engine_list:
            product.engine.add(CarEngine.objects.get(id=engine))

        for car in car_model_list:
            product.car_model.add(CarModel.objects.get(id=car))

        return product

    def update(self, instance, validated_data):

        cross_data = validated_data.pop("product_cross")
        # Менее Адский гемор по вложенной сериализации
        engine_data = validated_data.get("engine")
        try:
            engine_qs = CarEngine.objects.get(id=engine_data.id)
            instance.engine = engine_qs
        except:
            pass

        unit_data = validated_data.pop("unit")
        try:
            unit_qs = Units.objects.get(id=unit_data.id)
            instance.unit = unit_qs
        except:
            pass

        # Brand updating logic
        try:
            brand_qs = BrandsDict.objects.get(id=validated_data.get("brand").id)
            instance.brand = brand_qs
        except:
            pass

        # Car model update logic
        carmodel_data = validated_data.pop("car_model")
        car_model_list = [x.id for x in carmodel_data]
        car_model_qs = CarModel.objects.filter(model_product=instance.id)

        # Car Engine update logic
        car_engine_data = validated_data.pop("engine")
        car_engine_list = [_.id for _ in car_engine_data]
        car_engine_qs = CarEngine.objects.filter(car_related_engine=instance.id)

        instance.brand = validated_data.get("brand", instance.brand)
        instance.name = validated_data.get("name", instance.name)
        instance.name2 = validated_data.get("name2", instance.name2)
        instance.cat_number = validated_data.get("cat_number", instance.cat_number)
        instance.oem_number = validated_data.get("oem_number", instance.oem_number)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.one_c_id = validated_data.get("one_c_id", instance.one_c_id)
        instance.active = validated_data.get("active", instance.active)
        instance.save()

        for car in car_model_qs:
            instance.car_model.remove(car)
        for car_l in car_model_list:
            instance.car_model.add(CarModel.objects.get(id=car_l))

        # Car engine making references
        for engine in car_engine_qs:
            instance.engine.remove(engine)
        for eng in car_engine_list:
            instance.engine.add(CarEngine.objects.get(id=eng))

        # Creating or updating crosses
        for cross in cross_data:
            objct, created = Cross.objects.update_or_create(
                product=instance,
                cross=cross["cross"],
                defaults={"product": instance, "cross": cross["cross"]},
            )

        return instance


class ProductDescriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for product description has to get, post, put, delete methods.
    Defenantly must be ModelViewSet serialiser
    """

    class Meta:
        model = ProductDescription
        fields = ["id", "text", "product"]


class MerchantImagesSerilizer(serializers.ModelSerializer):
    """
    For Merchant images only
    """

    class Meta:
        model = ProductImage
        fields = ["images"]

    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        photo_url = obj.img800.url
        if photo_url:
            return settings.SITE_URL + photo_url
        else:
            return []


class MerchangSerializer(serializers.ModelSerializer):
    """
    Serializer for merchant and other Ads API
    """

    title = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    category_id = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    has_photo = serializers.SerializerMethodField()
    images = MerchantImagesSerilizer(many=True)
    car_model = serializers.SerializerMethodField()
    engine = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()

    def get_brand(self, obj):

        if obj.brand:
            return obj.brand.brand

    def get_description(self, obj):
        if obj.description:
            soup = BeautifulSoup(obj.description, "html.parser")
            text = soup.get_text()
            return text
        else:
            return ""

    def get_title(self, obj):
        return obj.name

    def get_video(self, obj):
        videos = obj.product_video.all()
        if len(videos):
            return videos[0].url
        else:
            return ""

    def get_price(self, obj):
        stock = obj.product_stock.all()
        if stock:
            return stock[0].price
        else:
            return None

    def get_stock(self, obj):
        stock = obj.product_stock.all()
        if stock:
            return stock[0].quantity
        else:
            return 0

    def get_category_id(self, obj):
        category = obj.category.all()
        if category:
            return category[0].id
        else:
            return None

    def get_category_name(self, obj):
        category = obj.category.all()
        if category:
            return category[0].name
        else:
            return None

    def get_has_photo(self, obj):
        return obj.have_photo

    def get_car_model(self, obj):
        car_model = obj.car_model.all()
        if len(car_model):
            return car_model[0].carmake.name + " " + car_model[0].name
        else:
            return ""

    def get_engine(self, obj):
        engine = obj.engine.all()
        if engine:
            return engine[0].name
        else:
            return ""

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "cat_number",
            "brand",
            "one_c_id",
            "car_model",
            "description",
            "images",
            "video",
            "price",
            "stock",
            "category_id",
            "category_name",
            "engine",
            "has_photo",
            "created_date",
            "updated_date",
        ]
