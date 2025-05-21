import pytest
from rest_framework import serializers
from events.serializers import EventUserSerializer, EventSerializer
from events.tests.fixtures import organizer, participant1, participant2, event
from django.utils import timezone


@pytest.mark.django_db
class TestUserSerializer:
    """Test class for UserSerializer."""

    def test_user_serialization(self, organizer):
        """Test serializing a user."""
        serializer = EventUserSerializer(organizer)
        data = serializer.data

        assert data["id"] == organizer.id
        assert data["username"] == "organizer"
        assert data["email"] == "organizer@example.com"
        assert data["is_organizer"] is True


@pytest.mark.django_db
class TestEventSerializer:
    """Test class for EventSerializer."""

    def test_event_serialization(self, event, participant1, participant2):
        """Test serializing an event with participants."""
        # Add participants to the event
        event.participants.add(participant1, participant2)

        serializer = EventSerializer(event)
        data = serializer.data

        assert data["id"] == event.id
        assert data["title"] == "Test Event"
        assert data["description"] == "This is a test event"
        assert data["location"] == "Online"
        assert data["organizer"]["username"] == "organizer"
        assert len(data["participants"]) == 2
        assert data["participants"][0]["username"] in ["participant1", "participant2"]
        assert data["participants"][1]["username"] in ["participant1", "participant2"]
        assert "participant_ids" not in data  # write_only field

    def test_event_deserialization_valid(self, organizer, participant1, participant2):
        """Test deserializing valid event data with participant_ids."""
        data = {
            "title": "New Event",
            "description": "A new test event",
            "date": timezone.now().isoformat(),
            "location": "Offline",
            "participant_ids": [participant1.id, participant2.id],
        }

        serializer = EventSerializer(data=data, context={"request": None})
        assert serializer.is_valid(), serializer.errors
        event = serializer.save(organizer=organizer)

        assert event.title == "New Event"
        assert event.description == "A new test event"
        assert event.location == "Offline"
        assert event.organizer == organizer
        assert event.participants.count() == 2
        assert participant1 in event.participants.all()
        assert participant2 in event.participants.all()

    def test_event_deserialization_no_participants(self, organizer):
        """Test deserializing event data without participant_ids."""
        data = {
            "title": "No Participants Event",
            "description": "Event without participants",
            "date": timezone.now().isoformat(),
            "location": "Online",
        }

        serializer = EventSerializer(data=data, context={"request": None})
        assert serializer.is_valid(), serializer.errors
        event = serializer.save(organizer=organizer)

        assert event.title == "No Participants Event"
        assert event.description == "Event without participants"
        assert event.location == "Online"
        assert event.organizer == organizer
        assert event.participants.count() == 0

    def test_event_deserialization_invalid_participant_ids(self, organizer):
        """Test deserializing event data with invalid participant_ids."""
        data = {
            "title": "Invalid Event",
            "description": "Event with invalid participant",
            "date": timezone.now().isoformat(),
            "location": "Online",
            "participant_ids": [999],  # Non-existent user ID
        }

        serializer = EventSerializer(data=data, context={"request": None})
        assert not serializer.is_valid()
        assert "participant_ids" in serializer.errors
