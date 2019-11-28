from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from account.models import MyUser

@admin.register(MyUser)
class MyUserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'login_method', 'password', 'avatar', 'nickname',)}),
    )