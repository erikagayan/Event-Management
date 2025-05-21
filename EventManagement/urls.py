import debug_toolbar
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/events/", include("events.urls", namespace="events")),
    path("api/users/", include("users.urls", namespace="users")),

    path("__debug__/", include(debug_toolbar.urls)),
]
