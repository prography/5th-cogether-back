from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from account import views

app_name = 'account'

router = DefaultRouter()
router.register(r'', views.MyUserViewSet, 'account')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('login/github/', views.github_login, name='github-login'),
    path('login/github/callback/', views.github_login_callback, name='github-login-callback'),
    path('', include(router.urls)),
]
