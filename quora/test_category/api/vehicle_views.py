from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from test_category.models import Years, Vehicle, Makes
from test_category.api.vehicle_serializers import YearsSerializer, VehicleSerializer, MakesSerializer


class YearsView(generics.ListAPIView):
    # queryset = Categories.objects.all()
    queryset = Years.objects.all()
    serializer_class = YearsSerializer
    paginator = None
    permission_classes = [AllowAny]


class MakesView(generics.ListAPIView):
    queryset = Makes.objects.all()

    serializer_class = MakesSerializer
    paginator = None
    permission_classes = [AllowAny]


class VehicleView(viewsets.ModelViewSet):
    lookup_field = 'slug'
    # queryset = Categories.objects.all()
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    paginator = None
    permission_classes = [AllowAny]


class VehiclesBySlugView(generics.ListCreateAPIView):
    queryset = Vehicle.objects.all()

    serializer_class = VehicleSerializer
    paginator = None
    permission_classes = [AllowAny]

    def get_queryset(self):
        make = self.kwargs.get('make')
        if make:
            return self.queryset.filter(make=Makes.objects.get(name=make))
        else:
            return self.queryset
