from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet, basename='event')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')
router.register(r'meal-plans', views.MealPlanViewSet, basename='meal-plan')
router.register(r'meal-slots', views.MealSlotViewSet, basename='meal-slot')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserAPIView.as_view(), name='register'),
]
