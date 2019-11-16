from rest_framework import serializers

from event.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tag = TagSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'host', 'content', 'category',
                  'photo', 'created_at', 'updated_at', 'start_at',
                  'end_at', 'external_link', 'location', 'tag']

