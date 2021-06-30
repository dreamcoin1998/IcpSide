from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),   #注册
    path('verification_request/phone/', views.get_phone_verification_code),
    path('verification_request/email/', views.get_email_verification_code),
    path('login/phone/', views.login_phone),
    path('login/email/', views.login_email),
    path('login/email/', views.change_passswd_pnone),
]