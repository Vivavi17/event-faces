from rest_framework.serializers import ModelSerializer, ReadOnlyField

from .models import Event, Location


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ("id", "name")


class EventSerializer(ModelSerializer):
    location_name = ReadOnlyField(source="location.name")

    class Meta:
        model = Event
        fields = ("id", "name", "date", "status", "location", "location_name")
