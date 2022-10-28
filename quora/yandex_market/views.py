from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import GetStockSerializer
from product.models import Stock
from datetime import timedelta, datetime
from django.conf import settings


def createResponse(stock, warehouseId):
    now = datetime.now()
    delta = timedelta(hours=2)
    mydate = now - delta

    sku = {
        "sku": stock.product.id,
        "warehouseId": warehouseId,
        "items": [
            {"type": "FIT", "count": stock.quantity, "updatedAt": mydate},
        ],
    }
    return sku


class GetStock(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            token = request.META.get("HTTP_AUTHORIZATION")

            id_list = request.data.get("skus") or []
            warehouseId = request.data.get("warehouseId")
            qs = Stock.objects.filter(product__id__in=id_list)
            response = {"skus": [createResponse(x, warehouseId) for x in qs]}

            serializer = GetStockSerializer(response)
            if token == settings.YANDEX_MARKET_TOKEN:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": "You are must be authorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            return Response({"error": "Bad Request"}, status.HTTP_400_BAD_REQUEST)
