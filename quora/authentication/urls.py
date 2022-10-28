from django.contrib import admin
from django.urls import path
from .views import (
    LoginAPIView,
    RegisterView,
    VerifyEmailView,
    PasswordTokenCheckAPIView,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/", VerifyEmailView.as_view(), name="activate"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("reset/", RequestPasswordResetEmail.as_view(), name="reset"),
    path("newpassword/", SetNewPasswordAPIView.as_view(), name="newpassword"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "reset/<str:uidb64>/<str:token>/",
        PasswordTokenCheckAPIView.as_view(),
        name="reset-confirm",
    ),
]
