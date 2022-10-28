from django.urls import path, include
from .views import OrderAPIView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", OrderAPIView, basename="orders")


urlpatterns = [
    path("", include(router.urls)),
]
