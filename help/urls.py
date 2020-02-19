from django.urls import path, include

from rest_framework.routers import DefaultRouter

from help import views


app_name = 'help'

router = DefaultRouter()
router.register(r'me', views.QuestionViewSet, basename='me')
router.register(r'img', views.HelpImageViewSet, basename='img')

urlpatterns = [
    path('', include(router.urls)),
]