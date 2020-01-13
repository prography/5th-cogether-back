from django.db import models

from django_cleanup import cleanup

from cogether.utils import uuid_name_upload_to


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    photo = models.ImageField(upload_to=uuid_name_upload_to)
    original_url = models.URLField(unique=True)


MANUAL = 'manual'
USERREQUEST = 'user_request'
FESTA = 'festa_crawling'
MEETUP = 'meetup_crawling'
EVENTUS = 'eventus_crawling'
FACEBOOK = 'facebook_crawling'

EVENT_SOURCE = [
    (MANUAL, '사이트에서 직접 입력'),
    (USERREQUEST, '사용자 요청'),
    (FESTA, 'FESTA 크롤링'),
    (MEETUP, 'MEETUP 크롤링'),
    (EVENTUS, 'EVENTUS 크롤링'),
    (FACEBOOK, 'FACEBOOK 크롤링'),
]

EVENT_RELATED_TO_DEVELOPMENT = 'development'
EVENT_NOT_RELATED_TO_DEVELOPMENT = 'not_development'
UNCLASSIFIED_EVENTS = 'unclassified_events'


EVENT_STATUS = [
    (EVENT_RELATED_TO_DEVELOPMENT, '개발 행사'),
    (EVENT_NOT_RELATED_TO_DEVELOPMENT, '비개발 행사'),
    (UNCLASSIFIED_EVENTS, '미분류 행사'),
]


@cleanup.ignore
class DevEvent(models.Model):
    original_identity = models.IntegerField(blank=True, default=1)
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(
        max_length=30, choices=EVENT_SOURCE, default=MANUAL)
    status = models.CharField(
        max_length=30, choices=EVENT_STATUS, default=UNCLASSIFIED_EVENTS)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title
