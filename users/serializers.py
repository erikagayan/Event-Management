from typing import Any, Dict
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        # password only for reading; won't be displayed during serialization
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def create(self, validated_data: Dict[str, Any]) -> User:
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_organizer=validated_data.get("is_organizer", False),
        )
        return user

    def update(self, instance: User, validated_data: Dict[str, Any]) -> User:
        # Extracts password, removes it from dictionary
        password = validated_data.pop("password", None)

        # Remaining keys and values
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Check password
        if password is not None:
            validate_password(password, instance)
            instance.set_password(password)

        instance.save()
        return instance
