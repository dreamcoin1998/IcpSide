from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/', views.create),   # 新增产品
    path('update/', views.update),   # 新增产品
]