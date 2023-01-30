from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import DockerForm
import random,socket,os
from django.db import IntegrityError

@login_required(login_url='login')
def main(request):
    user = request.user
    checkDocker = Docker.objects.filter(user=user).exists()
    dockerList = Docker.objects.filter(user=user)
    username = request.user.username
    return render(request,'dashboard.html',{'username':username,'dockerList':dockerList,'checkDocker':checkDocker})

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
            try:
                docker = Docker(subdomain=subdomain, repository=repository, software=software, dbadmin=dbadmin, dbpassword=dbpassword, user=user)
                docker.save()
                success = "The website was successfully created"
                return render(request,'form.html',{'form':form,'success':success})
            except IntegrityError:
                    error = "Error: subdomain already exists"
                    return render(request,'form.html',{'form':form,'error':error})
    else:
        form = DockerForm()
    return render(request,'form.html',{'form':form})


def stopDocker(request, id):
    docker = Docker.objects.get(id=id)
    docker.is_active = False
    docker.save()
    return redirect('main')


def startDocker(request, id ):
    docker = Docker.objects.get(id=id)
    docker.is_active = True
    docker.port = choosePort()
    docker.save()
    return redirect('main')


def choosePort():
    s = socket.socket()
    while True:
        port = random.randint(8000, 9000)
        try:
            s.bind(("", port))
            s.close()
            return port
        except OSError:
            # Si el puerto está en uso, volvemos a intentar con otro puerto
            continue
