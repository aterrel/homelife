from rest_framework import viewsets, generics, permissions
from .models import Event, Recipe
from .serializers import EventSerializer, RecipeSerializer, UserSerializer
from django.contrib.auth.models import User

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class UserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer
