from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.serializers import UserAddressSerializer, UserDisplaySerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from users.models import CustomUser, UserAdresses
from rest_framework import status


class CurrentUserAPIVeiw(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDisplaySerializer
    paginator = None


class AddressesViewSet(viewsets.ModelViewSet):
    queryset = UserAdresses.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer
    paginator = None

    def list(self, request, *args, **kwargs):
        try:

            user = request.GET.get("user")
            queryset = self.queryset.filter(user=CustomUser.objects.get(id=user))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                "User not found in users views line 34",
                status=status.HTTP_404_NOT_FOUND,
            )


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        def hasImage(object):
            return hasattr(object, "profile")

        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data["token"])
        return Response(
            {
                "token": token.key,
                "user": {
                    "id": token.user.id,
                    "username": token.user.username,
                    "email": token.user.email,
                    "image": token.user.profile.image.url
                    if token.user.profile.image
                    else None
                    if hasImage(token.user)
                    else None,
                },
            }
        )
