from django.urls import path, include

from rest_framework.routers import DefaultRouter

from event import views


app_name = 'event'

router = DefaultRouter()
router.register(r'', views.DevEventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]
