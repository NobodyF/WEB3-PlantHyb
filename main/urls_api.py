# main/urls_api.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import PlantViewSet

router = DefaultRouter()
router.register(r'plants', PlantViewSet, basename='plant')

urlpatterns = [
    path('', include(router.urls)),
]
