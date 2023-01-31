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
            port = choosePort()
            try:
                dockerCreation(subdomain,port,dbadmin,dbpassword,user)
                reverseProxy(port,subdomain,user)
                docker = Docker(subdomain=subdomain, repository=repository, software=software, dbadmin=dbadmin, dbpassword=dbpassword,user=user,port=port)
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
    user = docker.user
    subdomain = docker.subdomain
    docker.is_active = False
    os.system(f"docker-compose -f /home/samuel/hostingfolders/{user}/{subdomain}/docker-compose.yml stop")
    docker.save()
    return redirect('main')


def startDocker(request, id ):
    docker = Docker.objects.get(id=id)
    user = docker.user
    subdomain = docker.subdomain
    docker.is_active = True
    os.system(f"docker-compose -f /home/samuel/hostingfolders/{user}/{subdomain}/docker-compose.yml up -d")
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
            continue


def dockerCreation(subdomain,port,dbuser,dbpassword,user):
    os.makedirs(f'/home/samuel/hostingfolders/{user}/{subdomain}')
    with open(f"/home/samuel/hostingfolders/{user}/{subdomain}/docker-compose.yml", "w") as f:
        f.write(f"""
        version: '3'

        services:
            db:
                image: mariadb:10.3.9
                volumes:
                    - data:/var/lib/mysql
                environment:
                    - MYSQL_ROOT_PASSWORD={dbpassword}
                    - MYSQL_DATABASE=wordpress
                    - MYSQL_USER={dbuser}
                    - MYSQL_PASSWORD={dbpassword}
            web:
                image: wordpress:4.9.8
                depends_on:
                    - db
                volumes:
                    - ./target:/var/www/html
                environment:
                    - WORDPRESS_DB_USER={dbuser}
                    - WORDPRESS_DB_PASSWORD={dbpassword}
                    - WORDPRESS_DB_HOST=db
                ports:
                    - {port}:80

        volumes:
            data: 
        """)

def reverseProxy(port,subdomain,user):
    with open(f"/etc/nginx/sites-available/{subdomain}.conf", "w") as f:
        f.write("""
    server {{
    #Escucha en el puerto 80, ipv4.
    listen 80;

    #Aquí deberás introducir el nombre de tu dominio.
    server_name {0}.ehost.io;

    access_log            /var/log/nginx/everyhost.com.access.log;

    location / {{
        #La configuración del proxy.
        proxy_pass http://10.43.55.77:{1}/;
    }}
    }}
    """.format(subdomain,port))
    os.system(f"ln -s /etc/nginx/sites-available/{subdomain}.conf /etc/nginx/sites-enabled")
    os.system("sudo systemctl reload nginx")
    
