from rest_framework import serializers

from event.models import Category, DevEvent, Photo


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['photo']


def exist_category(value):
    try:
        Category.objects.get(name=value.get('name'))
    except:
        raise serializers.ValidationError('Does not exist category.')


class DevEventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=False, validators=[exist_category])
    photo = PhotoSerializer(read_only=False)

    class Meta:
        model = DevEvent
        fields = ['id', 'title', 'host', 'content', 'category',
                  'photo', 'created_at', 'updated_at', 'start_at',
                  'end_at', 'external_link', 'location', ]

    def create(self, validated_data):
        category_name = validated_data.pop('category').get('name')
        category = Category.objects.get(name=category_name)
        instance = DevEvent.objects.create(category=category, **validated_data)
        return instance
