from rest_framework import generics
from users.serializers import UserSerializer
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class CreateTokenView(TokenObtainPairView):
    """Create a new token for user"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    # return auth user
    def get_object(self):
        return self.request.user
