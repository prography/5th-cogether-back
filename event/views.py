from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from rest_framework import viewsets

from event.models import Event, Category
from event.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def list(self, request):
        category = self.request.query_params.get('category')

        if not category:
            return super(EventViewSet, self).list(request)
        category = category_exist_or_not(category)
        queryset = Event.objects.filter(category=category)
        if queryset:
            serializer = EventSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)


def category_exist_or_not(category):
    try:
        category = Category.objects.get(name=category)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return category
    