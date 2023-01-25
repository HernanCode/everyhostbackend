from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('login', views.loginPage,name="login"),
    path('signup', views.signupPage,name="signup"),
    path('dashboard', views.dashboard,name="dashboard"),
    path('logout', views.logoutUser, name="logout"),
    path("",views.home, name="home"),
    path("bar",views.bar, name="bar"),
    
]

