from urllib.parse import unquote

from rest_framework.decorators import permission_classes
from .helpers import RussianStemmer
from rest_framework import generics
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from product.forms import KeyWordForm
import operator
import json
from django.core import serializers
from functools import reduce
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q, Count
from product.models import (
    Product,
    Units,
    CarMake,
    CarModel,
    CarEngine,
    ProductImage,
    ProductVideos,
    Category,
    ProductDescription,
    ProductAttribute,
    ProductAttributeName,
)

from brands.models import BrandsDict
from product.api.serializers_site import (
    CategoryTreeSerializer,
    CategoryFirstLevelSerializer,
    MpttTestSerializer,
    GetSingleProductSerializer,
    GetCarModelSerializer,
    GetCarMakesSerializer,
    CategorySerializer,
)
from django.http import Http404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .helpers import modify_input_for_multiple_files
from rest_framework.permissions import AllowAny


# class CategoriesTreeList(generics.ListCreateAPIView):
#     '''

#     Recursive version

#     API View for category Tree view
#     recursively making json
#     It reseives all categories
#     '''
#     query = Q(id__gte=1, id__lte=20)
#     queryset = Category.objects.filter(query).exclude(parent__isnull=True).order_by('id')
#     serializer_class = CategoryTreeSerializer
#     permission_classes = [AllowAny]


class GetAllCategoriesFlat(generics.ListAPIView):
    """Getting all categories for all reasons in flat fashion"""

    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    pagination_class = None


class CategoriesTreeList(generics.ListCreateAPIView):
    """
    No Recursive for now
    API View for category Tree view
    recursively making json
    It reseives all categories
    """

    serializer_class = MpttTestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Here is sample of add_relative_count
        """
        queryset = Category.objects.add_related_count(
            Category.objects.get(id=1).get_children(),  # Queryset
            Product,  # Related model
            "category",  # Name of the foreignkey field
            "some_count",  # Name of the property added to the collection
            cumulative=True,
        )  # Cumulative or not.

        anc = queryset.get_ancestors(include_self=True)

        return queryset


class CategoriesListFirstLevel(generics.ListAPIView):
    """
    API View for category Tree view
    returns first level of categories
    """

    query = Q(id__gte=1, id__lte=20)
    queryset = (
        Category.objects.filter(query).exclude(parent__isnull=True).order_by("id")
    )
    serializer_class = CategoryFirstLevelSerializer
    permission_classes = [AllowAny]


class MpttTest(generics.ListAPIView):
    """
    API View for category Tree view
    returns first level of categories
    """

    serializer_class = MpttTestSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        query = Q(id__gte=1000, id__lte=2000)
        queryset = (
            Category.objects.filter(id=1).exclude(parent__isnull=True).order_by("id")
        )
        des = queryset.get_descendants(include_self=False)
        anc = queryset.get_ancestors(include_self=True)

        return des


class SingleProduct(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = GetSingleProductSerializer
    permission_classes = [AllowAny]


# class SingleProductC(generics.RetrieveAPIView):
#    serializer_class = GetSingleProductSerializer
#    permission_classes = [AllowAny]
#
#    def get_queryset(self):
#        queryset = Product.objects.get(one_c_id=self.kwargs['pk'])
#        print(queryset)
#        return queryset


class SingleProductC(APIView):
    """
    Class getting product by 1C id
    """

    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        try:
            queryset = Product.objects.get(one_c_id=pk)
            serializer = GetSingleProductSerializer(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"status": "Object is not Found"}, status=status.HTTP_404_NOT_FOUND
            )
            # return Response({'error': 'error'})


class GetCarModelList(generics.ListAPIView):
    """
    List of All Car Models
    """

    queryset = CarModel.objects.all()
    serializer_class = GetCarModelSerializer
    permission_classes = [AllowAny]


class GetCarModel(APIView):
    """
    Single car model havent used for now
    """

    permission_classes = [AllowAny]

    def get(self, request, pk):
        carModel = CarModel.objects.get(id=pk)
        serializer = GetCarModelSerializer(carModel)
        return Response(serializer.data)


class GetCarMakes(generics.ListAPIView):

    """
    Retrieve List of Car Models
    """

    queryset = CarMake.objects.all()
    serializer_class = GetCarMakesSerializer
    permission_classes = [AllowAny]


class ProductAnalogList(APIView):
    """
    API View for list for analogs
    Will select parts by same catalogue number
    """

    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        # category_list = request.GET.get('category', None).split(',')
        cat_number = request.GET.get("cat_number")

        try:
            products = (
                Product.objects.filter(cat_number__icontains=cat_number)
                .exclude(id=pk)
                .distinct()
            )

            serializer = GetSingleProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"status": "Objects are not Found"}, status=status.HTTP_404_NOT_FOUND
            )


class ProductRelatedListView(APIView):
    """
    API View for list for Related Products
    Later probably needs to change logic
    Now: getting products related by name
    Later: will getting products Wich relation
    written by hand
    """

    permission_classes = [AllowAny]

    def get(self, request, pk, format=None):
        prod_name = unquote(request.GET.get("product_name"))

        car_model = request.GET.get("car_model")
        search_list = prod_name.split(" ")

        search_word = RussianStemmer.stem(search_list[0])

        try:
            products = (
                Product.objects.filter(name__icontains=search_word, car_model=car_model)
                .distinct()
                .exclude(id=pk)[:12]
            )
            serializer = GetSingleProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"status": "Objects are not Found"}, status=status.HTTP_404_NOT_FOUND
            )
