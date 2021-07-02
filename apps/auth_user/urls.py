from django.contrib import admin
from django.urls import path
from auth_user import views
from utils.sensitives import detect_sensitives

urlpatterns = [
    path('register/', views.register),   #注册
    path('verification_request/phone/', views.get_phone_verification_code),
    path('verification_request/email/', views.get_email_verification_code),
    path('login/phone/', views.login_phone),
    path('login/email/', views.login_email),
    path('change_passswd_pnone/', views.change_passswd_pnone),
    path('change_passswd_email/', views.change_passswd_email),
    path('verification/phone/', views.change_phone),
    path('verification/email/', views.change_email),
    path('update_info/', views.update_info),
    path('detect/', detect_sensitives.detect),  # 敏感词检测
]