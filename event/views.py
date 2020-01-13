from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from event.models import Category, DevEvent
from event.serializers import DevEventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class DevEventViewSet(viewsets.ModelViewSet):
    queryset = DevEvent.objects.filter(status='development')
    serializer_class = DevEventSerializer
    pagination_class = StandardResultsSetPagination
    http_method_names = ['get', 'post']

    def get_queryset(self):
        queryset = DevEvent.objects.filter(status='development')
        category = self.request.query_params.get('category', None)
        title = self.request.query_params.get('title', None)
        if category is not None:
            category = get_object_or_404(Category, name=category)
            queryset = queryset.filter(category=category)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset.order_by('-start_at')

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        user = self.request.user
        event = get_object_or_404(DevEvent, pk=pk)
        if event in user.like_events.all():
            user.like_events.remove(event)
        else:
            user.like_events.add(event)
        return Response(DevEventSerializer(event).data)
