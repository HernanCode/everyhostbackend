from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.loginPage,name="login"),
    path('signup', views.signupPage,name="signup"),
    path('dashboard', views.dashboard,name="dashboard"),
    path('logout', views.logoutUser, name="logout"),
]
