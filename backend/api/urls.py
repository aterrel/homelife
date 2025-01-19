from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RecipeViewSet, UserAPIView

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserAPIView.as_view(), name='register'),
]
