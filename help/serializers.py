from rest_framework import serializers

from help.models import HelpCenter, HelpInfo


class HelpCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpCenter
        fields = ('id', 'contents', 'title', 'source',
                  'created_at', 'updated_at', 'status',
                  'answered_by', 'answer', 'user')
        read_only_fields = ('id', 'user')


class HelpInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpInfo
        fields = ('id', 'contents')
        read_only_fields = ('id',)
