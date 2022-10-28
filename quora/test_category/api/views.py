from collections import defaultdict
from rest_framework.decorators import action
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from .serializers import (
    CategoriesSerializer,
    DepthOneCategorySerializer,
    CategoriesSerializerfFlat,
    CategoriesSerializerfFlatForTestes,
    CategoriesSerializerRecursive,
)
from test_category.models import Categories, Product
from rest_framework.permissions import AllowAny
from .serializers_product import ProductSerializer
from django.db.models import Count


class CategoriesView(generics.ListAPIView):
    """
    FLAT-
    This view takes categories in flat fashon only get parent in there
    """

    # queryset = Categories.objects.all()
    queryset = Categories.objects.add_related_count(
        Categories.objects.all(), Product, "categories", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlat  # CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):

        depth = self.request.GET.get("depth")
        if depth and (depth == "1"):
            self.serializer_class = DepthOneCategorySerializer
            return self.queryset.filter(level__lte=0)

        else:
            return self.queryset.all()


class SingleCategorySlugView(generics.RetrieveAPIView):

    queryset = Categories.objects.add_related_count(
        Categories.objects.all(), Product, "categories", "count", cumulative=True
    )
    lookup_field = "slug"
    serializer_class = CategoriesSerializer
    permission_classes = [AllowAny]


class SingleProductView(viewsets.ReadOnlyModelViewSet):
    """
    Class Set for getting single product or set of products
    to show on category pages by category slug
    If no products in category dont pick up them
    """

    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    paginator = None

    def get_queryset(self):
        category = self.request.GET.get("category")
        if category:
            queryset = self.queryset.filter(
                categories__in=Categories.objects.filter(slug=category).get_descendants(
                    include_self=True
                )
            )
            return queryset
        return self.queryset


# View for testes with flat serialization
class CategoriesViewRecursive(generics.ListAPIView):
    """
    This class I made for testing recursive categories getting wit product count
    Further purpose will be for creating elasticsearch bulk insert models
    Created when experimented with elasticsearch
    """

    # queryset = Categories.objects.all()
    queryset = Categories.objects.add_related_count(
        Categories.objects.all(), Product, "categories", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerRecursive  # CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]


class CategoriesViewForTestes(generics.ListAPIView):
    # queryset = Categories.objects.all()
    queryset = Categories.objects.add_related_count(
        Categories.objects.all(), Product, "categories", "count", cumulative=True
    )

    serializer_class = CategoriesSerializerfFlatForTestes  # CategoriesSerializer
    paginator = None
    permission_classes = [AllowAny]
