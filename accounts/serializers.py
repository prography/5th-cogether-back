from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2']

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')

        if password1 and password2 and password1 != password2:
            raise ValueError('password mismatch')

        user = User.objects.create(username=validated_data['username'])
        user.set_password(password1)
        user.save()
        return user
