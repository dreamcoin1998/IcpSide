"""
设置admin页面

Creator: Gao Junbin
Update: 2021-07-01
"""
from django.contrib import admin
from .models import AccessLog


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):

    list_display = ("ip", "url", "datetime", "username")

