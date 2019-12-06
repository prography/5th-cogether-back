from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from account.models import MyUser

@admin.register(MyUser)
class MyUserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'login_method', 'password', 'avatar', 'social_avatar', 'nickname',)}),
    )