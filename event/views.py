from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from event.models import Category, DevEvent
from event.serializers import DevEventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DevEventViewSet(viewsets.ModelViewSet):
    queryset = DevEvent.objects.all()
    serializer_class = DevEventSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = DevEvent.objects.all()
        category = self.request.query_params.get('category', None)
        title = self.request.query_params.get('title', None)
        if category is not None:
            category = get_object_or_404(Category, name=category)
            queryset = queryset.filter(category=category)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset.order_by('-start_at')
