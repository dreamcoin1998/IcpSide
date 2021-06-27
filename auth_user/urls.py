from django.contrib import admin
from django.urls import path
from . import onAuth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',onAuth.register),   #注册
    path('verification_request/phone/',onAuth.get_phone_verification_code),
    path('verification_request/email/',onAuth.get_email_verification_code),
    path('login/phone/',onAuth.login_phone),
    path('login/email/',onAuth.login_email),
    path('login/email/',onAuth.change_passswd_pnone),
]