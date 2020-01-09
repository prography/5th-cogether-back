from django.contrib import admin
from event.models import Category, DevEvent, Photo


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(DevEvent)
class DevEventAdmin(admin.ModelAdmin):
    def set_events_status_to_development(self, request, queryset):
        rows_updated = queryset.update(status='development')
        self.message_user(
            request, "%s개의 이벤트가 성공적으로 개발 행사로 변경되었습니다." % rows_updated)

    set_events_status_to_development.short_description = "개발 행사로 변경하기"

    def set_events_status_to_not_development(self, request, queryset):
        rows_updated = queryset.update(status='not_development')
        self.message_user(
            request, "%s개의 이벤트가 성공적으로 비개발 행사로 변경되었습니다." % rows_updated)
    
    set_events_status_to_not_development.short_description = "비개발 행사로 변경하기"

    list_display = ['title', 'status', 'created_at', 'source']
    search_fields = ['title']
    fieldsets = (
        (None, {
            'fields': ('status', 'title', 'host', 'content', 'category', 'external_link')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('source', 'photo', 'original_identity',
                       'location', 'start_at', 'end_at',),
        })
    )
    actions = [set_events_status_to_development, set_events_status_to_not_development]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
