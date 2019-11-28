from account.models import MyUser

from rest_framework import viewsets
from rest_framework.decorators import APIView

from account.serializers import MyUserSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    serializer_class = MyUserSerializer
    queryset = MyUser.objects.all()
