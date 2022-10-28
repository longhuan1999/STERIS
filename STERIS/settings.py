"""
Django settings for STERIS project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'userInterface.apps.UserinterfaceConfig',
    'snowpenguin.django.recaptcha2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'STERIS.urls'

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

WSGI_APPLICATION = 'STERIS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'steris',
        'USER': 'steris',
        'PASSWORD': 'XXXXXXXXXXXXXXXX',
        'HOST': 'localhost',
        'PORT': '43306',
        #'OPTIONS': {'init_command': 'SET sql_mode="STRICT_TRANS_TABLES",default_storage_engine=INNODB;'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# STATIC_ROOT = os.path.join(BASE_DIR,'static')

# 邮件功能设置

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '2017083122@czie.edu.cn'
EMAIL_HOST_PASSWORD = 'XXXXXXXXXXXXXXXX'
DEFAULT_FROM_EMAIL = 'endless小龙的自考成绩查询系统<2017083122@czie.edu.cn>'


# Google reCaptcha v3 功能设置

# RECAPTCHA_PRIVATE_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# RECAPTCHA_PUBLIC_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# RECAPTCHA_DEFAULT_ACTION = 'generic'
# RECAPTCHA_SCORE_THRESHOLD = 0.5
# RECAPTCHA_FRONTEND_PROXY_HOST = 'https://recaptcha.net'
# RECAPTCHA_PROXY_HOST = 'https://recaptcha.net'


# Google reCaptcha v2 功能设置

RECAPTCHA_PRIVATE_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
RECAPTCHA_PUBLIC_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
RECAPTCHA_PROXY_HOST = 'https://recaptcha.net'


# Configuring django-csp

CSP_DEFAULT_SRC = ["'self'", "'unsafe-inline'", 'www.google.com', 'www.gstatic.cn', 'www.gstatic.com', 'recaptcha.net', 'fonts.googleapis.com', 'fonts.gstatic.com', 'wpa.qq.com']
CSP_IMG_SRC = ["'self'", 'data:', 'wpa.qq.com', 'pub.idqqimg.com']


# session 设置

# SESSION_COOKIE_NAME ＝ "key"            # Session的cookie保存在浏览器上时的key
# SESSION_COOKIE_PATH ＝ "/"              # Session的cookie保存的路径（默认）
# SESSION_COOKIE_DOMAIN = None            # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = True            # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True         # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 86400              # Session的cookie失效日期（2周）（数字为秒数）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST =  False     # 是否每次请求都保存Session，默认修改之后才保存（默认）
