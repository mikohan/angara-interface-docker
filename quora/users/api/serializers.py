from rest_framework import serializers
from users.models import CustomUser, UserAdresses


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdresses
        exclude = ("autouser",)
        extra_kwargs = {
            "zip_code": {"required": False, "allow_null": True},
            "city": {"required": False, "allow_null": True},
            "default": {"required": False, "allow_null": True},
        }


class UserDisplaySerializer(serializers.ModelSerializer):
    address_user = UserAddressSerializer(many=True, required=False)

    class Meta:
        model = CustomUser
        # fields = ("id", "email", "profile")
        exclude = (
            "password",
            "user_permissions",
            "groups",
            "is_superuser",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")

        user = CustomUser(username=username, email=email, password=password)
        user.save()
        return user

    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.image = validated_data.get("image", instance.image)
        instance.save()

        return instance
