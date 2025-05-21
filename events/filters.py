from django.db.models import Q
from events.models import Event
from django_filters import rest_framework as filters

class EventFilter(filters.FilterSet):
    """Filters for model Event"""

    # The user enters a string by which to search for an event.
    search = filters.CharFilter(
        method="filter_search",
        label="Search by name, description or location"
    )

    date_from = filters.DateTimeFilter(
        field_name="date",
        lookup_expr="gte",
        label="Start date (inclusive)"
    )

    date_to = filters.DateTimeFilter(
        field_name="date",
        lookup_expr="lte",
        label="End date (inclusive)"
    )

    class Meta:
        model = Event
        fields = ["search", "date_from", "date_to"]

    def filter_search(self, queryset, name, value):
        """Filtering by text in the title, description, location fields"""
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value) |
            Q(location__icontains=value)
        )
