from django.contrib.auth import authenticate
from users.models import CustomUser as User
import os
import random
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from django.conf import settings


def generate_username(name):

    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)
            print(registered_user.image.url)

            return {
                "id": registered_user.id,
                "username": registered_user.username,
                "email": registered_user.email,
                "tokens": registered_user.tokens(),
                "image": settings.SITE_URL + registered_user.image.url
                if registered_user.image
                else None,
            }

        else:
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )

    else:
        user_credentials = {
            "username": generate_username(name),
            "email": email,
            "password": settings.SOCIAL_SECRET,
        }
        user = User.objects.create_user(**user_credentials)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(email=email, password=settings.SOCIAL_SECRET)
        return {
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "tokens": new_user.tokens(),
            "image": None,
        }
