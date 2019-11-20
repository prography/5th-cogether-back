# Django
from django.contrib.auth.models import User

# Django-Rest-Framework
from rest_framework import viewsets
from rest_framework.decorators import APIView

# Local Django
from accounts.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
