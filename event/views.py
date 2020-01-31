from django.shortcuts import get_object_or_404

from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from event.models import Category, DevEvent
from event.serializers import DevEventSerializer
from event import get_new_events_from_festa as festa_crawling, get_new_events_from_meetup as meetup_crawling
from event import send_email
from datetime import datetime, timedelta


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

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def crawling(self, request):
        start_time = datetime.now()
        festa_message = festa_crawling.save_new_events_from_festa_dev_group()
        meetup_message = meetup_crawling.save_new_events_from_meetup_dev_group(
            meetup_crawling.korea_meetup_dev_group)
        return Response({'message': '크롤링이 종료되었습니다.',
                         'detail': {'festa': festa_message,
                                    'meetup': meetup_message,
                                    'start_time': str(start_time),
                                    'during': str(datetime.now() - start_time)}},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminUser])
    def email_to_subscriber(self, request):
        send_email.test_email()
        return Response({'message': '구독자들에게 메일이 전송되었습니다.'})

from django.views.generic import ListView

class EventListView(ListView):
    model = DevEvent
    template_name = 'event/cogether_subscribe_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.today()
        created_last_week_event = DevEvent.objects.filter(
            created_at__range=(today + timedelta(days=-7), today))
        start_this_week_event = DevEvent.objects.filter(
            start_at__range=(today, today + timedelta(days=7)))
        context['created_last_week_event'] = created_last_week_event
        context['start_this_week_event'] = start_this_week_event
        return context
