from rest_framework import serializers
from users.models import CustomUser
from users.models import CustomUser as User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User already exists")

        username = attrs.get("username", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters"
            )
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ("token",)


class LoginAPIViewSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        return {"access": user.tokens()["access"], "refresh": user.tokens()["refresh"]}

    class Meta:
        model = User
        fields = ["email", "password", "username", "tokens", "image", "id"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Inalid credentials try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Account is not activated")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
            "id": user.id,
        }


class ResetPasswordEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=6)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=255, write_only=True)
    uidb64 = serializers.CharField(min_length=1)
    token = serializers.CharField(min_length=1)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password", "")
            uidb64 = attrs.get("uidb64", "")
            token = attrs.get("token", "")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link in invalid", 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed("The reset link in invalid", 401)
