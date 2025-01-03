from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
