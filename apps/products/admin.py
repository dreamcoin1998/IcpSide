"""
设置admin页面

Creator: Gao Junbin
Update: 2021-07-02
"""
from django.contrib import admin
from .models import ProductType, ProductInfo


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('product_type_id', 'type_name')


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "product_type", "product_detail", "create_time", "update_time", "user", "price", "inventory", "images")
