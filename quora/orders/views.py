from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import permissions
from .models import Orders
from .serializers import OrderSerializer
from rest_framework.response import Response
from users.models import AutoUser, CustomUser
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


class OrderAPIView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    paginator = None

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     serializer = self.serializer_class
    #     data = serializer.data
    #     print(dir(data))
    #     send_mail(
    #         "Test email in order",
    #         "Message from test order",
    #         "mikohan1@gmail.com",
    #         ["angara99@gmail.com"],
    #         fail_silently=False,
    #     )
    #     return response

    def list(self, request, *args, **kwargs):
        user = request.GET.get("user", None)
        autouser = request.GET.get("autouser", None)

        queryset = self.queryset
        try:
            if user:
                queryset = self.queryset.filter(user=CustomUser.objects.get(id=user))
            elif autouser:
                queryset = self.queryset.filter(
                    autouser=AutoUser.objects.get(id=autouser)
                )
            else:
                return Response("You must be authorized", status.HTTP_401_UNAUTHORIZED)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                "Orders for that usern is not exists yet",
                status=status.HTTP_404_NOT_FOUND,
            )
