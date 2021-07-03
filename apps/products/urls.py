from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path('create', views.create),  # 新增产品
    path('update', views.update),  # 新增产品
    path('<int:product_id>', views.get_product_info),  # 产品详情
    path('types', views.product_types),  # 所有产品类型列表
    path('user', views.my_products),  # 获取用户已发布的产品信息列表
    path('type', views.products_type),  # 根据类型id获取该类型的产品列表
    path('recommond', views.recommond),  # 推荐产品列表
    path('all', views.get_all_products),  # 获取所有产品
    path('search', views.search_products),  # 搜索产品
]
