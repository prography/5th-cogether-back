from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

MyUser = get_user_model()


class MyUserSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True)
    password1 = serializers.CharField(max_length=100, write_only=True,
                                      style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=100, write_only=True,
                                      style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'password1', 'password2']

    def create(self, validated_data):
        password1 = validated_data.pop('password1', '')
        password2 = validated_data.pop('password2', '')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError('비밀번호와 비밀번호 확인이 일치하지 않습니다.')

        try:
            user = MyUser.objects.get(username=validated_data['username'])
            already_login_method = user.login_method
            raise serializers.ValidationError(
                'This email has already been used to login ' + already_login_method)
        except MyUser.DoesNotExist:
            user = MyUser.objects.create(username=validated_data['username'])
            user.set_password(password1)
            user.save()
            return user


class PasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(max_length=100, write_only=True,
                                      style={'input_type': 'password'})
    password1 = serializers.CharField(max_length=100, write_only=True,
                                      style={'input_type': 'password'})
    password2 = serializers.CharField(max_length=100, write_only=True,
                                      style={'input_type': 'password'})

    class Meta:
        model = MyUser
        fields = ['current_password', 'password1', 'password2']

    def validate(self, data):
        password1 = data['password1']
        password2 = data['password2']

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({'password1': '새 비밀번호와 비밀번호 확인이 일치하지 않습니다.'})
        return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['avatar'] = ''
        if user.avatar.name:
            token['avatar'] = user.avatar.url
        token['social_avatar'] = user.social_avatar
        token['nickname'] = user.nickname
        token['username'] = user.username
        token['login_method'] = user.login_method

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
