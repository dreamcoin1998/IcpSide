from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create),   # 新增产品
    path('update/', views.update),   # 新增产品
    path(r'(\d+)', views.get_product_info),  ##v1.0：版本1；product：产品模块
    path(r'types/', views.product_types),  ##所有产品类型列表
    path(r'user$', views.my_products),    # 获取用户已发布的产品信息列表
    path(r'type$', views.products_type),    # •	/v1.0/product/recommond?count=&page=
    path(r'recommond$', views.recommond),    # •	/v1.0/product/recommond?count=&page=
    path(r'all$', views.get_all_products),    # 获取所有产品
    path(r'search$', views.search_products),    # 搜索产品
]