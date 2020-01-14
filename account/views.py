import requests
import json
import re
import os
import urllib.parse
from uuid import uuid4

from django.conf import settings
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.http.response import HttpResponseBadRequest

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import APIView, action
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from account.serializers import (MyUserSerializer, MyTokenObtainPairSerializer,
                                PasswordSerializer, ProfileSerializer)
from account.permissions import IsEmailloginUser
from event.serializers import DevEventSerializer


MyUser = get_user_model()
GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        user = self.request.user
        queryset = user.like_events.all()
        serializer = DevEventSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[IsEmailloginUser], url_path='update-password', url_name='update-password')
    def update_password(self, request, pk=None):
        user = self.request.user
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.validated_data['current_password']):
                return Response({'message': '현재 비밀번호가 다릅니다.'}, status=status.HTTP_403_FORBIDDEN)
            user.set_password(serializer.validated_data['password1'])
            user.save()
            return Response({'message': '비밀번호가 변경되었습니다.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='retrieve-profile', url_name='retrieve-profile')
    def retrieve_profile(self, request):
        user = self.request.user
        return Response(ProfileSerializer(user).data)

    @action(detail=False, methods=['patch'],  permission_classes=[IsAuthenticated], url_path='update-profile', url_name='update-profile')
    def update_profile(self, request):
        user = self.request.user
        serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            user.subscribe = serializer.validated_data['subscribe']
            user.save()
            print(user.subscribe)
            return Response({'message': '메일 구독 기능이 변경되었습니다.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def github_login(request):
    url = 'https://github.com/login/oauth/authorize/'
    payload = {
        'client_id': GITHUB_CLIENT_ID,
        'scope': 'read:user',
    }
    params = urllib.parse.urlencode(payload)
    url_for_code_request = f"{url}?{params}"
    return redirect(url_for_code_request)


@api_view(('GET',))
def github_login_callback(request):
    code = request.GET.get('code', '')
    payload = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
    }
    headers = {'Accept': 'application/json', }
    res_for_access_token = requests.post(
        'https://github.com/login/oauth/access_token',
        data=payload,
        headers=headers)
    res_json = res_for_access_token.json()

    access_token = res_json.get('access_token')
    res = requests.get(
        'https://api.github.com/user',
        headers={'Authorization': 'token ' + access_token})
    if res.status_code != 200:
        return HttpResponseBadRequest('GitHub login failed for unknown reasons.' + res.status_code)
    user_json = res.json()

    if user_json.get('email') is None:
        return Response({'message': '해당 계정은 Public email이 등록되어 있지 않습니다. https://github.com/settings/profile 에서 Public email을 등록해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = MyUser.objects.get(username=user_json.get('email'))
        if user.login_method == 'github':
            refresh = MyTokenObtainPairSerializer.get_token(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'This email has already been used to login ' + user.login_method + ' Please login using ' + user.login_method}, status=status.HTTP_400_BAD_REQUEST)
    except MyUser.DoesNotExist:
        social_avatar = user_json.get('avatar_url')
        user = MyUser.objects.create(
            username=user_json.get('email'),
            nickname=user_json.get('login'),
            login_method='github',
            social_avatar=social_avatar)
        refresh = MyTokenObtainPairSerializer.get_token(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
