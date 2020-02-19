from rest_framework import serializers

from help.models import Question, HelpContentImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpContentImage
        fields = ('id', 'image')


class QuestionSerializer(serializers.ModelSerializer):
    # capture = CaptureSerializer(read_only=False)

    class Meta:
        model = Question
        fields = ('id', 'contents', 'title', 'type',
                  'created_at', 'updated_at', 'status',
                  'answer')
        read_only_fields = ('id',)
