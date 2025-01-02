from rest_framework.viewsets import ModelViewSet
from .models import Event, Recipe
from .serializers import EventSerializer, RecipeSerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
