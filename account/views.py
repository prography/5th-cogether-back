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
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import MyUserSerializer


MyUser = get_user_model()
GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


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

    try:
        user = MyUser.objects.get(username=user_json.get('email'))
        if user.login_method == 'github':
            refresh = RefreshToken.for_user(user)
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
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
