from django.db import models

# Create your models here.

class User(models.Model):   ## 用户表
    userid=models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    introduction = models.CharField(max_length=100,blank=True,null=True)
    verification = models.BooleanField(auto_created=False)
    create_time = models.DateTimeField(auto_now_add=True)
    avatar = models.IntegerField()

class Verification_Code(models.Model):  ## 验证码表
    verificationId=models.AutoField(primary_key=True, null=False)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False)
    update_time = models.DateTimeField(auto_now_add=True)
    verification_type = models.CharField(max_length=100, null=False)
    
class Sensitives(models.Model):  ## 敏感词表
    sensitive_words = models.CharField(max_length=100, null=False)
    create_time = models.DateTimeField(auto_now_add=True, null=False)
