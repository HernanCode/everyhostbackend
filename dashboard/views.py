from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def main(request):
    username = request.user.username
    return render(request,'dashboard.html',{'username':username})

def userLogout(request):
    logout(request)
    return redirect('../login')
