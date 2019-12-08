from django.contrib import admin
from event.models import (Category, FestaCrawling, MeetupCrawling,
                          EventusCrawling, FacebookCrawling, UserrequestEvent,
                          WaitingEvent, DevEvent, NotDevEvent)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(FestaCrawling)
class FestaCrawlingAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetupCrawling)
class MeetupCrawlingAdmin(admin.ModelAdmin):
    pass


@admin.register(EventusCrawling)
class EventusCrawlingAdmin(admin.ModelAdmin):
    pass


@admin.register(FacebookCrawling)
class FacebookCrawlingAdmin(admin.ModelAdmin):
    pass


@admin.register(UserrequestEvent)
class UserrequestEventAdmin(admin.ModelAdmin):
    pass


@admin.register(WaitingEvent)
class WaitingEventAdmin(admin.ModelAdmin):
    pass


@admin.register(DevEvent)
class DevEventAdmin(admin.ModelAdmin):
    pass


@admin.register(NotDevEvent)
class NotDevEvent(admin.ModelAdmin):
    pass
