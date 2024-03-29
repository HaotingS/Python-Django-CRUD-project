"""coin_price_form URL Configuration

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
from django.urls import path, include
from pages.views import input_view, list_view, home, logout, register, login, search, delete_coin
from django.views.generic.base import TemplateView

urlpatterns = [

    path('input/', input_view, name= 'input'),
    path('input/list/', list_view, name = 'list'),
    path('admin/', admin.site.urls), 
    path('', home, name = 'home'),
    path('', include("django.contrib.auth.urls")),
    path('register/', register, name = 'register'),
    path('logout/', logout, name = 'logout'),
    path("login/", login, name = 'login'),
    path('input/list/searched_results/', search, name='search'),
    path('delete/<int:id>/', delete_coin, name = 'delete'),
]
