import pytest
from events.models import Event
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory
from events.tests.fixtures import organizer, participant1, participant2, event


@pytest.mark.django_db
class TestEventViewSet:
    """Test class for EventViewSet."""

    @pytest.fixture
    def client(self):
        """Fixture to create an APIClient."""
        return APIClient()

    @pytest.fixture
    def request_factory(self):
        """Fixture to create an APIRequestFactory."""
        return APIRequestFactory()

    def test_create_event_as_organizer(
        self, client, organizer, participant1, participant2
    ):
        """Test creating an event as an organizer."""
        client.force_authenticate(user=organizer)
        data = {
            "title": "New Event",
            "description": "A new test event",
            "date": timezone.now().isoformat(),
            "location": "Offline",
            "participant_ids": [participant1.id, participant2.id],
        }

        response = client.post("/api/events/", data, format="json")

        assert response.status_code == 201
        assert response.data["title"] == "New Event"
        assert response.data["organizer"]["username"] == "organizer"
        assert len(response.data["participants"]) == 2
        assert response.data["participants"][0]["username"] in [
            "participant1",
            "participant2",
        ]
        assert response.data["participants"][1]["username"] in [
            "participant1",
            "participant2",
        ]

    def test_create_event_as_non_organizer(self, client, participant1):
        """Test creating an event as a non-organizer raises PermissionDenied."""
        client.force_authenticate(user=participant1)
        data = {
            "title": "New Event",
            "description": "A new test event",
            "date": timezone.now().isoformat(),
            "location": "Offline",
        }

        response = client.post("/api/events/", data, format="json")
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )

    def test_retrieve_event_list(self, client, event, participant1):
        """Test retrieving the list of events."""
        event.participants.add(participant1)
        response = client.get("/api/events/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["title"] == "Test Event"
        assert response.data[0]["participants"][0]["username"] == "participant1"

    def test_retrieve_event_detail(self, client, event, participant1):
        """Test retrieving a single event's details."""
        event.participants.add(participant1)
        response = client.get(f"/api/events/{event.id}/")

        assert response.status_code == 200
        assert response.data["title"] == "Test Event"
        assert response.data["organizer"]["username"] == "organizer"
        assert response.data["participants"][0]["username"] == "participant1"

    def test_update_event_as_organizer(self, client, event, organizer, participant2):
        """Test updating an event as the organizer."""
        client.force_authenticate(user=organizer)
        data = {
            "title": "Updated Event",
            "description": "Updated test event",
            "date": timezone.now().isoformat(),
            "location": "Offline",
            "participant_ids": [participant2.id],
        }

        response = client.put(f"/api/events/{event.id}/", data, format="json")

        assert response.status_code == 200
        assert response.data["title"] == "Updated Event"
        assert response.data["location"] == "Offline"
        assert len(response.data["participants"]) == 1
        assert response.data["participants"][0]["username"] == "participant2"

    def test_update_event_as_non_organizer(self, client, event, participant1):
        """Test updating an event as a non-organizer raises PermissionDenied."""
        client.force_authenticate(user=participant1)
        data = {
            "title": "Updated Event",
            "description": "Updated test event",
            "date": timezone.now().isoformat(),
            "location": "Offline",
        }

        response = client.put(f"/api/events/{event.id}/", data, format="json")
        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )

    def test_delete_event_as_organizer(self, client, event, organizer):
        """Test deleting an event as the organizer."""
        client.force_authenticate(user=organizer)
        response = client.delete(f"/api/events/{event.id}/")

        assert response.status_code == 204
        assert not Event.objects.filter(id=event.id).exists()

    def test_delete_event_as_non_organizer(self, client, event, participant1):
        """Test deleting an event as a non-organizer raises PermissionDenied."""
        client.force_authenticate(user=participant1)
        response = client.delete(f"/api/events/{event.id}/")

        assert response.status_code == 403
        assert (
            response.data["detail"]
            == "You do not have permission to perform this action."
        )
