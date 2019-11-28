from rest_framework import serializers

from event.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = DevEvent
        fields = ['id', 'title', 'host', 'content', 'category',
                  'photo', 'created_at', 'updated_at', 'start_at',
                  'end_at', 'external_link', 'location',]

