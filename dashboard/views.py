from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import DockerForm

@login_required(login_url='login')
def main(request):
    username = request.user.username
    return render(request,'dashboard.html',{'username':username})

def userLogout(request):
    logout(request)
    return redirect('../login')

@login_required(login_url='login')
def dockerForm(request):
    if request.method == "POST":
        form = DockerForm(request.POST)
        if form.is_valid():
            subdomain = form.cleaned_data['subdomain']
            software = form.cleaned_data['software']
            repository = form.cleaned_data['repository']
            dbadmin = form.cleaned_data['dbadmin']
            dbpassword = form.cleaned_data['dbpassword']
            user = request.user
            docker = Docker(subdomain=subdomain, repository=repository, software=software, dbadmin=dbadmin, dbpassword=dbpassword, user=user)
            docker.save()

    else:
        form = DockerForm()
    return render(request,'form.html',{'form':form})

        
