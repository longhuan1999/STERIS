"""STERIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from userInterface import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('account_settings', views.account_settings, name='account_settings'),
    path('subscribe_change_on', views.subscribe_change_on, name='subscribe_change_on'),
    path('subscribe_change_off', views.subscribe_change_off, name='subscribe_change_off'),
    path('scores', views.scores, name='scores'),
    path('user_logs', views.user_logs, name='user_logs'),
    path('help', views.help, name='help'),
    path('test', views.test, name='test'),
]
