from rest_framework import serializers

from event.models import Event, Tag, Category


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
        fields = ['title', 'host', 'content', 'category', 'image',
                  'created_at', 'updated_at', 'start_at', 'end_at',
                  'external_link', 'location', 'tag']
