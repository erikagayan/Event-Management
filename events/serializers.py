from rest_framework import serializers
from events.models import Event
from django.contrib.auth import get_user_model

User = get_user_model()


# Serializer for the User model (to display information about the organizer)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_organizer"]


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="participants",
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "organizer",
            "participants",
            "participant_ids"
        ]
