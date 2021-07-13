from django.db import models
from image.models import ImagePath
from django.contrib.contenttypes.fields import GenericRelation


class Yonghu(models.Model):  ## 用户表
    userid = models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=20, null=False, verbose_name='用户名')
    password = models.CharField(max_length=100, null=False, verbose_name='密码')
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机')
    introduction = models.CharField(max_length=100, blank=True, null=True, verbose_name='个人介绍')
    verification = models.BooleanField(auto_created=False, verbose_name='是否已认证', default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    avatar = GenericRelation(ImagePath)

    @property
    def avatar_url(self):
        if self.avatar.all():
            return self.avatar.all().first().url
        return ""

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username + "_id_" + str(self.userid)


class VerificationCode(models.Model):  # 验证码表，后期修改不用下划线
    verificationId = models.AutoField(primary_key=True, null=False)
    code_type = (
        ('phone', "手机号"),
        ('email', "邮箱")
    )
    verification_type = models.CharField(max_length=10, null=False, choices=code_type, verbose_name="验证类型")
    phoneOrEmail = models.CharField(max_length=100, verbose_name="邮箱或手机号")
    code = models.CharField(max_length=6, null=False, verbose_name="验证码")
    update_time = models.DateTimeField(auto_now=True, blank=True, verbose_name="发送时间")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name


class Sensitives(models.Model):  ## 敏感词表
    sensitive_words = models.CharField(max_length=100, null=False)
    create_time = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        verbose_name = "敏感词"
        verbose_name_plural = verbose_name
