from django.contrib import admin
from django.urls import path
from . import onAuth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',onAuth.register),   #注册
    path('verification_request/phone/',onAuth.get_phone_verification_code)
]