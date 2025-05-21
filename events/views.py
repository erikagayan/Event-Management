from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from events.models import Event
from events.serializers import EventSerializer
from events.permissions import IsOrganizerOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user

        # Check that the current user is the organizer
        if not user.is_organizer:
            raise PermissionDenied("Only organizers can create events")
        serializer.save(organizer=user)

    def perform_update(self, serializer):
        user = self.request.user

        # Check that the user is the event organizer
        if user != serializer.instance.organizer:
            raise PermissionDenied("Only organizers can create events")
        serializer.save()
