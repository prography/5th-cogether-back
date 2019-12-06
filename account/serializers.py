from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer, PasswordField


MyUser = get_user_model()

class MyUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)
    password1 = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password1', 'password2']

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('password mismatch')

        try:
            user = MyUser.objects.get(username=validated_data['username'])
            already_login_method = user.login_method
            raise serializers.ValidationError('This email has already been used to login ' + already_login_method)
        except MyUser.DoesNotExist:
            user = MyUser.objects.create(username=validated_data['username'])
            user.set_password(password1)
            user.save()
            return user
