from django.utils.encoding import smart_bytes, smart_str
from rest_framework.permissions import AllowAny
from users.models import CustomUser as User
from rest_framework import generics, status, views
from .renderers import UserRenderer

from .serializers import (
    EmailVerificationSerializer,
    RegisterSerializer,
    LoginAPIViewSerializer,
    ResetPasswordEmailResetSerializer,
    SetNewPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator


"""
Need to replace site url for activation email to frontend site
"""


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data["email"])

        token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        absUrl = f"{settings.FRONTEND_URL}/account/activate?token={str(token)}"
        # relativeLink = reverse("activate")
        # absUrl = "http://" + current_site + relativeLink + "?token=" + str(token)
        email_body = f"""
        Hi {user.username} Use link below to activate your account \n
        {absUrl} 
        """
        data = {
            "email_recepient": user.email,
            "email_body": email_body,
            "email_subject": f"Activate your account at {settings.FRONTEND_URL}",
        }
        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(views.APIView):
    serializer_class = EmailVerificationSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):

        token = request.GET.get("token")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_201_CREATED
            )

        except jwt.ExpiredSignatureError as indentifier:
            return Response(
                {"error": "Activation link Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.DecodeError as indentifier:
            return Response(
                {"error": "Invalid token request new one"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginAPIViewSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = {"request": request, "data": request.data}

        serializer = self.serializer_class(data=data)
        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            absUrl = f"{settings.FRONTEND_URL}/account/newpassword/?uid={uidb64}&token={token}"
            email_body = f"""
            Hi {user.username} Use link below to reset your password \n
            {absUrl} 
            """
            data = {
                "email_recepient": user.email,
                "email_body": email_body,
                "email_subject": f"Reset your password at {settings.FRONTEND_URL}",
            }
            Util.send_email(data)

        return Response(
            {"success": "We are sent you a link to reset your password"},
            status.HTTP_200_OK,
        )


class PasswordTokenCheckAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailResetSerializer
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token in not valid, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            return Response(
                {
                    "success": True,
                    "message": "Credentials Valid",
                    "uidb64": uidb64,
                    "token": token,
                }
            )

        except Exception as e:
            return Response(
                {"error": "Token in not valid, please request a new one"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"success": True, "message": "Password reset success"})
