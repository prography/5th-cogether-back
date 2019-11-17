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
    category = CategorySerializer(read_only=True)
    # tag = TagSerializer(many=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'host', 'content', 'category',
                  'photo', 'created_at', 'updated_at', 'start_at',
                  'end_at', 'external_link', 'location', 'tag']
                  
    def create(self, validated_data):
        category_id = self.context.get('view').request.data['category']
        validated_data['category_id'] = category_id
        return super().create(validated_data)



