from django.urls import path, include, re_path
from users.api.views import AddressesViewSet, CurrentUserAPIVeiw, CustomObtainAuthToken

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", CurrentUserAPIVeiw, basename="user")
router.register(r"addresses", AddressesViewSet, basename="addresses")


urlpatterns = [
    # path("user/", CurrentUserAPIVeiw.as_view(), name="current-user"),
    path("", include(router.urls)),
    path("authenticate/", CustomObtainAuthToken.as_view(), name="current-user"),
]
