from rest_framework import serializers

from help.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'contents', 'title', 'type',
                  'created_at', 'updated_at', 'status',
                  'answer')
        read_only_fields = ('id',)
