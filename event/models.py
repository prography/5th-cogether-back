from django.db import models

from cogether.utils import uuid_name_upload_to


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=100)
    host = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, upload_to=uuid_name_upload_to)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(blank=True)
    end_at = models.DateTimeField(blank=True)
    external_link = models.URLField(blank=True, default='')
    location = models.CharField(max_length=200, blank=True, default='')
    tag = models.ManyToManyField('Tag', through='EventTag')

    class Meta:
        ordering = ['start_at']

    def __str__(self):
        return self.title


class EventTag(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(str(self.event), str(self.tag))
