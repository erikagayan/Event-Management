import pytest
from events.models import Event
from events.tests.fixtures import organizer, participant1, participant2, event


@pytest.mark.django_db
class TestEventModel:
    """Test class for the Event model."""

    def test_event_creation(self, event, organizer):
        """Test creating an event with an organizer."""
        assert event.title == "Test Event"
        assert event.description == "This is a test event"
        assert event.location == "Online"
        assert event.organizer == organizer
        assert event.participants.count() == 0
        assert Event.objects.count() == 1

    def test_event_add_participants(self, event, participant1, participant2):
        """Test adding and removing participants to an event."""
        # Add participants
        event.participants.add(participant1, participant2)
        assert event.participants.count() == 2
        assert participant1 in event.participants.all()
        assert participant2 in event.participants.all()

        # Remove one participant
        event.participants.remove(participant1)
        assert event.participants.count() == 1
        assert participant1 not in event.participants.all()
        assert participant2 in event.participants.all()

    def test_event_str(self, event):
        """Test the string representation of an event."""
        assert str(event) == "Test Event"

    def test_event_meta(self):
        """Test the Meta attributes of the Event model."""
        meta = Event._meta
        assert meta.verbose_name == "Event"
        assert meta.verbose_name_plural == "Events"
