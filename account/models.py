from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as AuthUserManager

from cogether.utils import uuid_name_upload_to

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class MyUserManager(AuthUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        return super().create_superuser(username, email, password, **extra_fields)


class MyUser(AbstractUser):
    """
    Custom User Model
    """

    LOGIN_EMAIL = 'email'
    LOGIN_GITHUB = 'github'
    LOGIN_KAKAO = 'kakao'
    LOGIN_NAVER = 'naver'
    LOGIN_GOOGLE = 'google'

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, 'Email'),
        (LOGIN_GITHUB, 'Github'),
        (LOGIN_KAKAO, 'Kakao'),
        (LOGIN_NAVER, 'Naver'),
        (LOGIN_GOOGLE, 'Google'),
    )

    avatar = models.ImageField(
        upload_to=uuid_name_upload_to, null=True, blank=True)
    nickname = models.CharField(max_length=20, default='', blank=True)
    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    objects = MyUserManager()
