import requests
import json
import re
import urllib.parse
from uuid import uuid4

from django.shortcuts import redirect
from django.http.response import HttpResponseBadRequest
from django.core.files.base import ContentFile

from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, renderer_classes

from account.serializers import MyUserSerializer
from account.models import MyUser


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()


def github_login(request):
    url = 'https://github.com/login/oauth/authorize/'
    payload = {
        'client_id': '7ca42cd1744a91380d69',
        'scope': 'read:user',
        'redirect_uri': 'http://127.0.0.1:8000/account/login/github/callback/',
    }
    params = urllib.parse.urlencode(payload)
    url_for_code_request = f"{url}?{params}"
    return redirect(url_for_code_request)


@api_view(('GET',))
def github_login_callback(request):
    code = request.GET.get('code', '')
    payload = {
        'client_id': '7ca42cd1744a91380d69',
        'client_secret': 'b1bd734a65259b18f18882fab23df7c727434e32',
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
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'message': 'This email has already been used to login ' + user.login_method + ' Please login using ' + user.login_method}, status=status.HTTP_400_BAD_REQUEST)
    except MyUser.DoesNotExist:
        social_avatar = user_json.get('avatar_url')
        user = MyUser.objects.create(
            username=user_json.get('email'),
            nickname=user_json.get('login'),
            login_method='github',
            social_avatar=social_avatar)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})
