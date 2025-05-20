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
    organizer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_organizer=True),
        source="organizer",
        write_only=True,
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
            "organizer_id",
        ]
