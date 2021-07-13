from django.contrib import admin
from django.urls import path
from detect import views

urlpatterns = [
    path('sensitives/', views.detect),   # 敏感词检测接口
]