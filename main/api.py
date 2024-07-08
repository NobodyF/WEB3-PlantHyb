from rest_framework import viewsets
from .models import Plant
from .serializers import PlantSerializer

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
