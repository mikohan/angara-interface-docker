from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers_react import RedGetSingleProductSerializer

from rest_framework.response import Response
from rest_framework import status
from product.models import Product


class RedSingleProductAPI(APIView):
    """
    Class getting product by slug and return serilized product for
    Product Card
    """

    permission_classes = [AllowAny]

    def get(self, request, slug, format=None):
        queryset = Product.objects.get(slug=slug)
        serializer = RedGetSingleProductSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # try:
        #     queryset = Product.objects.get(slug=slug)

        #     serializer = RedGetSingleProductSerializer(queryset)
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # except:
        #     return Response(
        #         {"status": "Object is not Found"}, status=status.HTTP_404_NOT_FOUND
        #     )
        # return Response({"error": "error"})
