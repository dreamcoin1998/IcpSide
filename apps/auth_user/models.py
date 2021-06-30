from django.db import models

# Create your models here.

class User(models.Model):   ## 用户表
    userid=models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=20, null=False, verbose_name = '用户名')
    password = models.CharField(max_length=100, null=False, verbose_name = '密码')
    email = models.CharField(max_length=100,blank=True,null=True, verbose_name = '邮箱')
    phone = models.CharField(max_length=20,blank=True,null=True, verbose_name = '手机')
    introduction = models.CharField(max_length=100,blank=True,null=True, verbose_name = '个人介绍')
    verification = models.BooleanField(auto_created=False, verbose_name = '是否已认证')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name = '创建时间')
    # avatar = models.OneToOneField(verbose_name = '头像')
    # a = models.FileField()

class Verification_Code(models.Model):  ## 验证码表，后期修改不用下划线
    verificationId=models.AutoField(primary_key=True, null=False)
    verification_type = models.CharField(max_length=100, null=False)
    phoneOrEmail = models.IntegerField()
    code = models.CharField(max_length=6, null=False)
    update_time = models.DateTimeField(auto_now_add = True, blank=True)
    
    # update_time = models.DateTimeField(auto_now_add=True)
    
class Sensitives(models.Model):  ## 敏感词表
    sensitive_words = models.CharField(max_length=100, null=False)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
