from django.db import models

from cogether.utils import uuid_name_upload_to


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


MANUAL = 'manual'
USERREQUEST = 'user_request'
FESTA = 'festa_crawling'
MEETUP = 'meetup_crawling'
EVENTUS = 'eventus_crawling'
FACEBOOK = 'facebook_crawling'

DATA_SOURCE = [
    ('manual', 'manual'),
    ('user', 'user_request'),
    ('festa', 'festa_crawling'),
    ('meetup', 'meetup_crawling'),
    ('eventus', 'eventus_crawling'),
    ('facebook', 'facebook_crawling'),
]


class FestaCrawling(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=FESTA)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class MeetupCrawling(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=MEETUP)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class EventusCrawling(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=EVENTUS)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class FacebookCrawling(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=FACEBOOK)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class ManualEvent(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=MANUAL)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class UserrequestEvent(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    description = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=USERREQUEST)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class WaitingEvent(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=FACEBOOK)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class DevEvent(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=30, choices=DATA_SOURCE, default=USERREQUEST)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class NotDevEvent(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True,
                              upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    start_at = models.DateTimeField(blank=True, null=True)
    end_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    external_link = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    source = models.CharField(
        max_length=30, choices=DATA_SOURCE, default=USERREQUEST)

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title
