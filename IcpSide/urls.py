"""IcpSide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from ..apps.products import views as pviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1.0/auth/', include('apps.auth_user.urls')),  ##v1.0：版本1；auth：用户认证模块
    path('v1.0/products/', include('apps.products.urls')),  ##v1.0：版本1；products：产品模块
    path(r'v1.0/product/(\d+)', pviews.get_product_info),  ##v1.0：版本1；product：产品模块
    path('v1.0/product_types/', pviews.product_types),  ##产品类型列表•	/v1.0/my_products?count=&page=
    path(r'/v1.0/my_products$', pviews.my_products),    # •	/v1.0/products/type?id=&count=&page=
    path(r'/v1.0/products/type$', pviews.products_type),    # •	/v1.0/product/recommond?count=&page=
    path(r'/v1.0/product/recommond$', pviews.recommond),    # •	/v1.0/product/recommond?count=&page=
    path(r'/v1.0/products$', pviews.get_all_products),    # •	/v1.0/products?count=&page=
    path(r'/v1.0/products$', pviews.search_products),    # •	/v1.0/products?product_name=&count=&page=
]
