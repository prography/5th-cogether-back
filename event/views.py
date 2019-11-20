# Django
from django.shortcuts import get_object_or_404

# Django-Rest-Framework
from rest_framework import generics, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# Local Django
from event.models import Category, Event
from event.serializers import EventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Event.objects.all()
        category = self.request.query_params.get('category', None)
        if category is not None:
            category = get_object_or_404(Category, name=category)
            queryset = queryset.filter(category=category)
        return queryset
