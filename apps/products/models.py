from django.db import models
from django.db.models.deletion import CASCADE
import auth_user.models
import auth_user

# Create your models here.

class Product_Type(models.Model):   ## 产品类型表
    product_type_id = models.AutoField(primary_key=True, null=False)
    type_name = models.CharField(max_length=20, null=False)
    
class Product_Info(models.Model):  ## 产品信息表
    id = models.AutoField(primary_key=True, null=False)
    product_name = models.CharField(max_length=6, null = False)
    product_type_id = models.ForeignKey(Product_Type, null = True)
    product_detail = models.CharField(max_length=500, null = False)
    create_time = models.DateTimeField(auto_now_add=True, null = False)
    update_time = models.DateTimeField(auto_now = True, null = False)
    userid = models.ForeignKey(auth_user.models.User, on_delete=CASCADE)
    price = models.FloatField(null = False)
    inventory = models.IntegerField(null=False)