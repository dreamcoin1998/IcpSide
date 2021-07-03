"""
设置admin页面

Creator: Gao Junbin
Update: 2021-07-02
"""
from django.contrib import admin
from .models import Yonghu, VerificationCode, Sensitives


@admin.register(Yonghu)
class YonghuAdmin(admin.ModelAdmin):

    list_display = ('userid', 'username', 'email', 'phone', 'introduction', "avatar_url", 'create_time')


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):

    list_display = ("verificationId", "code_type", "phoneOrEmail", "code", "update_time")


@admin.register(Sensitives)
class Sensitives(admin.ModelAdmin):

    list_display = ("sensitive_words", "create_time")

