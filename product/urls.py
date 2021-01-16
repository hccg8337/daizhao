"""daizhao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

from product import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('go/', views.go, name="go"),
    path('back/', views.back, name="back"),
    path('edit/', views.edit, name="edit"),
    path('add/', views.add, name="add"),
    path('users/', views.list_users, name="users"),
    path('users/add/', views.add_user, name="add_user"),
    path('users/edit/', views.edit_user, name="edit_user"),
    path('', views.index, name="index"),
]
