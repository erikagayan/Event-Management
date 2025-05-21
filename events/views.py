from events.models import Event
from rest_framework import viewsets
from events.filters import EventFilter
from events.serializers import EventSerializer
from events.utils import send_notification_email
from events.permissions import IsOrganizerOrReadOnly
from rest_framework.exceptions import PermissionDenied


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]
    filterset_class = EventFilter

    def perform_create(self, serializer):
        user = self.request.user

        # Check that the current user is the organizer
        if not user.is_organizer:
            raise PermissionDenied("Only organizers can create events")
        event = serializer.save(organizer=user)

        # Sending email to participants
        participant_ids = serializer.validated_data.get("participants", [])
        for participant in participant_ids:
            send_notification_email(event, participant)

    def perform_update(self, serializer):
        user = self.request.user

        # Check that the user is the event organizer
        if user != serializer.instance.organizer:
            raise PermissionDenied("Only organizers can create events")

        # We get the old list of participants
        old_participants = set(
            serializer.instance.participants.values_list("id", flat=True)
        )
        event = serializer.save()

        # We receive a new list of participants
        new_participant_ids = set(
            p.id for p in serializer.validated_data.get("participants", [])
        )

        # Sending email to participants
        added_participant_ids = new_participant_ids - old_participants
        for participant_id in added_participant_ids:
            participant = event.participants.get(id=participant_id)
            send_notification_email(event, participant)
