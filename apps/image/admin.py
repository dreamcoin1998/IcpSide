"""
设置admin页面

Creator: Gao Junbin
Update: 2021-07-02
"""
from django.contrib import admin
from .models import ImagePath


@admin.register(ImagePath)
class ImagePathAdmin(admin.ModelAdmin):

    list_display = ("id", "url", "content_type", "object_id")

