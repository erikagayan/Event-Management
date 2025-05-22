import pytest
from django.contrib.auth import get_user_model
from events.models import Event
from django.utils import timezone

User = get_user_model()


@pytest.fixture
def organizer():
    """Fixture to create an organizer user."""
    return User.objects.create_user(
        username="organizer",
        email="organizer@example.com",
        password="securepassword123",
        is_organizer=True,
    )


@pytest.fixture
def participant1():
    """Fixture to create the first participant user."""
    return User.objects.create_user(
        username="participant1",
        email="participant1@example.com",
        password="securepassword123",
        is_organizer=False,
    )


@pytest.fixture
def participant2():
    """Fixture to create the second participant user."""
    return User.objects.create_user(
        username="participant2",
        email="participant2@example.com",
        password="securepassword123",
        is_organizer=False,
    )


@pytest.fixture
def event(organizer):
    """Fixture to create an event with an organizer."""
    return Event.objects.create(
        title="Test Event",
        description="This is a test event",
        date=timezone.now(),
        location="Online",
        organizer=organizer,
    )
