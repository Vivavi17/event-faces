from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Event
from .serializers import EventSerializer


class EventPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class EventViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.select_related("location").order_by("date")
    serializer_class = EventSerializer
    pagination_class = EventPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["name", "status"]
    search_fields = ["name"]
    ordering_fields = ["date"]
