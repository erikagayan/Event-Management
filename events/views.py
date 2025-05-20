from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user

        # Check that the current user is the organizer
        if not user.is_organizer:
            raise PermissionDenied("Only organizers can create events")

        # Check that the organizer_id matches the current user
        organizer_id = serializer.validated_data.get('organizer').id
        if organizer_id != user:
            raise PermissionDenied("You can only create events on your own behalf.")

        serializer.save()
