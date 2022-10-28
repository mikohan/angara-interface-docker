from collections import defaultdict
import datetime
from django.db.models import Q
from rest_framework.decorators import action, permission_classes
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from product.api.serializers import ProductSerializer
from product.api.serializers_a77 import (
    ProductA77Serializer,
    ProductA77SerializerBase,
    ProductSiteMapSerializer,
)
from rest_framework import mixins
from product.api.serializers_a77 import (
    CategoriesSerializerfFlat,
)
from product.models import Category, Product
from rest_framework.permissions import AllowAny
from django.db.models import Count

from test_category.api.serializers import (
    DepthOneCategorySerializer,
    CategoriesSerializer,
)


class ProductSitemapView(generics.ListAPIView):
    """
    Return only slug of all products

    """

    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    paginator = None  # type: ignore
    serializer_class = ProductSiteMapSerializer


class CategoriesView(generics.ListAPIView):
    """
    FLAT-
    This view takes categories in flat fashon only get parent in there
    """

    # queryset = Categories.objects.all()
    queryset = Category.objects.add_related_count(  # type: ignore
        Category.objects.filter(parent=1), Product, "category", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlat  # CategoriesSerializer
    paginator = None  # type: ignore
    permission_classes = [AllowAny]

    def get_queryset(self):

        depth = self.request.GET.get("depth")
        if depth and (depth == "1"):
            self.serializer_class = DepthOneCategorySerializer
            return self.queryset.filter(level__lte=0)

        else:
            return self.queryset.all()


class SingleCategorySlugView(generics.RetrieveAPIView, mixins.RetrieveModelMixin):

    queryset = Category.objects.add_related_count(  # type: ignore
        Category.objects.all(), Product, "category", "count", cumulative=True
    )
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]
    model = Product


class GetProductBySlugView(generics.RetrieveAPIView):
    """
    Class retreive single product by slug

    """
    lookup_field = "slug"
    serializer_class = ProductA77Serializer
    permission_classes = [AllowAny]
    queryset = Product.objects.all()





class GetProductsByCatNumbers(APIView):
    """Get all parts by array of cat numbers"""

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """Getting array and serilizing qyeryset"""
        numbers = request.GET.getlist("numbers")
        numbers = set([x for x in numbers if x])
        print(numbers)

        qs = Product.objects.filter(cat_number__in=numbers).distinct()
        serializer = ProductA77Serializer(qs, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GetProductByCatNumber(APIView):
    """Getting product for cat number for redirect"""

    permission_classes = [AllowAny]
    serializer_class = ProductA77SerializerBase

    def get(self, request, *args, **kwargs):
        cat_number = self.kwargs.get("cat_number")
        qs = Product.objects.filter(cat_number=cat_number).first()
        serializer = self.serializer_class(qs)
        return Response(serializer.data, status.HTTP_200_OK)


class GetProductByOneCId(generics.RetrieveAPIView):
    """Get product by one c id for redirect"""

    permission_classes = [AllowAny]
    model = Product
    queryset = Product.objects.all()
    lookup_field = "one_c_id"
    serializer_class = ProductA77SerializerBase


class HomePageFeaturesView(generics.ListAPIView):
    """
    Endpoint for home page all stuff
    """

    serializer_class_product = ProductA77SerializerBase
    # serializer_class_blog = BlogA77Serializer
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    # lookup_field = "car_model__slug"

    def get_queryset_latest_arrival(self):
        slug = self.kwargs.get("slug")
        qs = (
            self.queryset.filter(product_image__isnull=False)
            .distinct()
            .order_by("-created_date")
        )
        if slug and slug != "home":
            qs = qs.filter(car_model__slug=slug)
        return qs[:8]

    def get_queryset_sale(self):
        slug = self.kwargs.get("slug")
        qs = (
            self.queryset.filter(
                Q(product_image__isnull=False)
                & Q(product_stock__price__gt=1000)
                & Q(created_date__gt=self.last_year)
            )
            .distinct()
            .order_by("?")
        )
        if slug and slug != "home":
            qs = qs.filter(car_model__slug=slug)
        return qs[:24]

    def get_queryset_top_rated(self):
        slug = self.kwargs.get("slug")
        qs = self.queryset.filter(
            Q(product_image__isnull=False)
            & Q(product_stock__price__gt=1000)
            & Q(created_date__gt=self.last_year)
        ).order_by("?")
        if slug and slug != "home":
            qs = qs.filter(car_model__slug=slug)
        return qs[:3]

    def get_queryset_special_offers(self):
        slug = self.kwargs.get("slug")
        qs = self.queryset.filter(
            Q(product_image__isnull=False)
            & Q(product_stock__price__gt=1000)
            & Q(created_date__gt=self.last_year)
        ).order_by("?")
        if slug and slug != "home":
            qs = qs.filter(car_model__slug=slug)
        return qs[:3]

    def get_queryset_best_sellers(self):
        slug = self.kwargs.get("slug")
        qs = self.queryset.filter(
            Q(product_image__isnull=False)
            & Q(product_stock__price__gt=1000)
            & Q(created_date__gt=self.last_year)
        ).order_by("?")
        if slug and slug != "home":
            qs = qs.filter(car_model__slug=slug)
        return qs[:3]

    def list(self, request, *args, **kwargs):
        latest_serializer = self.serializer_class_product(
            self.get_queryset_latest_arrival(), many=True
        )
        sale_serializer = self.serializer_class_product(
            self.get_queryset_sale(), many=True
        )
        top_serializer = self.serializer_class_product(
            self.get_queryset_top_rated(), many=True
        )
        special_serializer = self.serializer_class_product(
            self.get_queryset_special_offers(), many=True
        )
        best_serializer = self.serializer_class_product(
            self.get_queryset_best_sellers(), many=True
        )
        return Response(
            {
                "latest": latest_serializer.data,
                "sale": sale_serializer.data,
                "top": top_serializer.data,
                "special": special_serializer.data,
                "best": best_serializer.data,
            }
        )
