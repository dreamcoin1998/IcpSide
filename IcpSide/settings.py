"""
Django settings for IcpSide project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
from .config import my_database
import sys
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# add search path
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y+xf52n1q#6(4hzc9vwlu2jts)6vs7y%(68hyoe1=mgz(&&s93'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # "simpleui",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # my apps
    'apps.auth_user',
    'apps.products',
    "apps.access_log",
    "apps.image",
    # "djcelery"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "utils.middlewares.access_log_record.AccessLogRecord"
]

ROOT_URLCONF = 'IcpSide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'IcpSide.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': my_database.name,
        'HOST': my_database.host, # 数据库地址，本机 ip 地址 127.0.0.1
        'PORT': my_database.port, # 端口
        'USER': my_database.user,  # 数据库用户名
        'PASSWORD': my_database.password, # 数据库密码
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# simpleui 配置
SIMPLEUI_HOME_ACTION = True


# COOKIE过期时间
EXPIRE_TIME = 90 * 365 * 24 * 60 * 60


# 邮箱配置
# 设置邮件域名
EMAIL_HOST = "smtp.exmail.qq.com"
# 设置端口号
EMAIL_PORT = 465
# 发件人邮箱
EMAIL_HOST_USER = 'gaojunbin@gaoblog.cn'
# 发件人姓名
EMAIL_WEBITE_NAME = '超级管理员'
# 发件人授权码
EMAIL_HOST_PASSWORD = 'xfYC4mkT2QLPuBQv'
# 设置是否启用安全链接
EMAIL_USE_SSL = True
#是否使用TLS安全传输协议
EMAIL_USE_TLS = False

ERROR_FROM = 'gaojunbin@gaoblog.cn'


# 第三方接口

