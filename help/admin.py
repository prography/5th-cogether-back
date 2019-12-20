from django.contrib import admin

from help.models import HelpCenter


# Register your models here.
class HelpAdmin(admin.ModelAdmin):
    list_display = ('source', 'title', 'contents')


admin.site.register(HelpCenter, HelpAdmin)
