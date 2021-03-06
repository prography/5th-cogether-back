from django.contrib import admin

from help.models import Question, Answer


# Register your models here.
class HelpAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'type')


admin.site.register(Question, HelpAdmin)
admin.site.register(Answer)
