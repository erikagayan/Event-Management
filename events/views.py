from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
