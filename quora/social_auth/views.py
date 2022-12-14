from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from .serializers import GoogleSocialSerializer
from rest_framework.response import Response


class GoogleAuthView(GenericAPIView):

    serializer_class = GoogleSocialSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        POST with "auth_token"
        Send and id_token as from google to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data["auth_token"]
        return Response(data, status=status.HTTP_200_OK)
