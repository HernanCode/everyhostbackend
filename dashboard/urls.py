from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.main,name="main"),
    path('addService', views.DeployForm, name="addService"),
    path('logout', views.userLogout, name="logout"),
    path('stopService/<str:service>/<int:idService>', views.stopService, name='stopService'),
    path('startService/<str:service>/<int:idService>', views.startService, name='startService'),
    path('deleteService/<int:id>/', views.deleteService, name='deleteService')
]

