from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets

from event.models import Event, Category
from event.serializers import EventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        category = self.request.query_params.get('category')
        if not category:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        if category:
            category = category_exist_or_not(category)
            if not category:
                return Response(status=status.HTTP_404_NOT_FOUND)            
            else:
                queryset = Event.objects.filter(category=category)
                if queryset:
                    page = self.paginate_queryset(queryset)
                    if page is not None:
                        serializer = self.get_serializer(page, many=True)
                        return self.get_paginated_response(serializer.data)
                    serializer = self.get_serializer(queryset, many=True)
                    return Response(serializer.data)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)


def category_exist_or_not(category):
    try:
        category = Category.objects.get(name=category)
    except Category.DoesNotExist:
        return False
    return category
