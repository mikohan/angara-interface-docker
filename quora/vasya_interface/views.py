from django.shortcuts import render
from rest_framework import viewsets
from .models import Rows
from .serializers import (
    RowsSerializer,
    CheckProductSerializer,
    CheckFolderSerializer,
    FolderListSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from product.models import Product
import os, re
from django.conf import settings


# helper function to get dir list
def getDonePhotos():
    # Scan all folders for make list
    path_to_photos = settings.PHOTO_FOLDER_FOR_AGES
    parts_list = []
    for foldOne in os.listdir(path_to_photos):
        for foldSecond in os.listdir(os.path.join(path_to_photos, foldOne)):
            m = re.search(r"(^\d+)_.+$", foldSecond)
            try:
                parts_list.append(m.group(1))
            except:
                pass

    return parts_list


class RowsView(viewsets.ModelViewSet):
    model = Rows

    queryset = Rows.objects.filter(isDone=False)
    # queryset = Rows.objects.all()
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class RowsViewDone(viewsets.ModelViewSet):
    model = Rows

    # queryset = Rows.objects.filter(isDone=False)
    queryset = Rows.objects.filter(isDone=True)
    serializer_class = RowsSerializer
    permission_classes = [AllowAny]
    paginator = None


class TestView(generics.ListCreateAPIView):
    queryset = Rows.objects.all()
    serializer_class = RowsSerializer


class CheckProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, one_c_id):
        try:
            product = Product.objects.get(one_c_id=one_c_id)
            serializer = CheckProductSerializer(product)
            return Response(serializer.data)
        except:
            return Response(
                {"Fail": "Product with that One C ID not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CheckMadeFoldersView(ListAPIView):

    queryset = Product.objects.all()
    # 1. Make list of all folders
    # 2. Make list of all products
    # 3. Make list of not done products

    serializer_class = CheckFolderSerializer
    permission_classes = [AllowAny]
    paginator = None

    def get_queryset(self):

        # Getting folders list
        part_list = getDonePhotos()

        have_photo_list = []
        product = Product.objects.all()
        for prod in product:
            if not prod.have_photo and str(prod.one_c_id) in part_list:
                have_photo_list.append(prod)

        return have_photo_list


class ProductNoPhotoListView(ListAPIView):
    """
    Gett all products with no photots
    """

    serializer_class = CheckFolderSerializer
    permission_classes = [AllowAny]
    paginator = None

    def get_queryset(self):
        queryset = Product.objects.all()
        dont_have_photo = []
        for prod in queryset:
            if not prod.have_photo:
                dont_have_photo.append(prod)
        return dont_have_photo


class FoldersHavePhotoView(APIView):
    """
    Gett all folders list with photos is made
    Later on needs to add some dir on server to upload files there
    and syncronizi it to all_photo also
    """

    permission_classes = [AllowAny]

    # Getting folders list
    def get(self, request):
        part_list = getDonePhotos()
        serializer = FolderListSerializer(part_list)
        return Response(serializer.data)
