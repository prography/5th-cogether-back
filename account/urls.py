from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from account import views, serializers

app_name = 'account'

router = DefaultRouter()
router.register(r'', views.MyUserViewSet, 'account')

urlpatterns = [
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    path('api-token-auth/', obtain_auth_token),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/github/', views.github_login, name='github-login'),
    path('login/github/callback/', views.github_login_callback, name='github-login-callback'),
    path('', include(router.urls)),
]
