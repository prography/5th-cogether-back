from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


class EventTagInline(admin.TabularInline):
    model = Event.tag.through


class TagAdmin(admin.ModelAdmin):
    inlines = [
        EventTagInline,
    ]

    search_fields = ['name']


class EventAdmin(admin.ModelAdmin):
    exclude = ('tag',)

    inlines = [
        EventTagInline,
    ]
    
    search_fields = ['title']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTag)
