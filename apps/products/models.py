from django.db import models
import auth_user.models
import auth_user

# Create your models here.


class ProductType(models.Model):
    """
    产品类型表
    """
    product_type_id = models.AutoField(primary_key=True, null=False)
    type_name = models.CharField(max_length=20, null=False)

    class Meta:
        verbose_name = "产品类型"
        verbose_name_plural = verbose_name


class ProductInfo(models.Model):
    """
    产品信息表
    """
    product_name = models.CharField(max_length=20, null=False, verbose_name="产品名称")
    product_type = models.ForeignKey(ProductType, null=True, on_delete=models.DO_NOTHING, verbose_name="产品类型")
    product_detail = models.CharField(max_length=500, null=False, verbose_name="产品详情")
    create_time = models.DateTimeField(auto_now_add=True, null=False, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, null=False, verbose_name="更新时间")
    user = models.ForeignKey(auth_user.models.Yonghu, on_delete=models.DO_NOTHING, verbose_name="发表用户")
    price = models.FloatField(null=False, verbose_name="价格")
    inventory = models.IntegerField(null=False, verbose_name="库存")

    class Meta:
        verbose_name = "产品信息"
        verbose_name_plural = verbose_name
