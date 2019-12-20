from django.urls import path, include

from rest_framework.routers import DefaultRouter

from help import views


app_name = 'help'

router = DefaultRouter()
router.register(r'info', views.HelpInfoViewSet, basename='info')
router.register(r'freq', views.FreqHelpCenterViewSet, basename='freq')
router.register(r'my-questions', views.MyHelpCenterViewSet, basename='my')

urlpatterns = [
    path('', include(router.urls)),
]