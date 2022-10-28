from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Manager
from django_resized import ResizedImageField
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


AUTH_PROVIDERS = {
    "facebook": "facebook",
    "google": "google",
    "twitter": "twitter",
    "email": "email",
}


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):

        if username is None:
            raise TypeError("Users sould have a useername")
        if email is None:
            raise TypeError("Users sould have a email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    # objects = Manager["User"]()

    def create_superuser(self, username, email, password=None):

        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    auth_provider = models.CharField(
        max_length=255, default=AUTH_PROVIDERS.get("email")
    )
    image = ResizedImageField(
        size=[100, 100],
        quality=75,
        crop=["middle", "center"],
        upload_to=settings.USER_IMAGES,
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    class Meta:
        verbose_name = "Ползователь"
        verbose_name_plural = "Ползователи"


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         CustomUser, on_delete=models.CASCADE, related_name="profile"
#     )
#     image = ResizedImageField(
#         size=[100, 100],
#         quality=75,
#         crop=["middle", "center"],
#         upload_to=settings.USER_IMAGES,
#         blank=True,
#         null=True,
#     )
#     phone = models.CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         verbose_name = "Профиль Пользователя"
#         verbose_name_plural = "Профили Пользователя"

#     def __str__(self):
#         return self.user.email


class AutoUser(models.Model):
    userId = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Автопользователь"
        verbose_name_plural = "Автопользователи"

    def __str__(self):
        return self.userId


class UserAdresses(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="address_user"
    )
    autouser = models.ForeignKey(
        AutoUser,
        on_delete=models.CASCADE,
        related_name="address_autouser",
        null=True,
        blank=True,
    )
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса Пользователя"

    def __str__(self):
        return f"{self.user.email} - {self.address}"

    def save(self, *args, **kwargs):
        if self.default == True:
            qs = UserAdresses.objects.filter(user=self.user).exclude(id=self.id)
            qs.update(default=False)
        super().save(*args, **kwargs)
