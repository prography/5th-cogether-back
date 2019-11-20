from django.urls import path, include

from rest_framework.routers import DefaultRouter

from event import views


router = DefaultRouter()
router.register(r'', views.EventViewSet, 'event')

urlpatterns = [
    path('', include(router.urls)),
]
