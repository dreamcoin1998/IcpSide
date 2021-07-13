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
from django.conf import settings  # 新增
from django.conf.urls import url  # 新增
from django.views import static  # 新增


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1.0/auth/', include('apps.auth_user.urls')),  ##v1.0：版本1；auth：用户认证模块
    path('v1.0/product/', include('apps.products.urls')),  ##v1.0：版本1；products：产品模块
    path('v1.0/detect/', include('apps.detect.urls')),  ##v1.0：版本1；detect：敏感词检测
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]
