from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.main,name="main"),
    path('logout', views.userLogout, name="logout"),
]

