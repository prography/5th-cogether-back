from django.urls import path, include

from rest_framework.routers import DefaultRouter

from event import views


app_name = 'event'

router = DefaultRouter()
router.register(r'', views.DevEventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('test/event/', views.EventListView.as_view()),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)