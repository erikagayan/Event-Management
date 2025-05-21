from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    """
    Permission that allows:
    - Everyone to view events (GET).
    - Only users with is_organizer=True to create events (POST).
    - Only the event organizer to edit (PUT, PATCH) or delete (DELETE) the event.
    """

    def has_permission(self, request, view):
        # Allow reading for everyone (including unauthorized)
        if request.method in permissions.SAFE_METHODS:
            return True

        # To create, update and delete, you need to be authorized and is_organizer=True
        return request.user.is_authenticated and request.user.is_organizer

    def has_object_permission(self, request, view, obj):
        # Allow reading for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # To edit and delete, check that the user is the event organizer
        return request.user == obj.organizer
