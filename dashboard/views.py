from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ServiceForm
import os
from django.db import IntegrityError
from . import k8sfiles as kube
import subprocess
import time

def checkDeploy(idUser,service,idService):
    if service == "mysql":
        deploy= f"client-{idUser}-mysql"
        command = f'kubectl get deployment {deploy} -o jsonpath="{{.status.readyReplicas}}"'
        print(deploy)
        commandOutput = os.popen(command).read().strip()
    else:
        deploy= f"client-{idUser}-{service}-{idService}"
        command = f'kubectl get deployment {deploy} -o jsonpath="{{.status.readyReplicas}}"'
        commandOutput = os.popen(command).read().strip()
    
    if commandOutput == "":
        return False
    else:
        return True

@login_required(login_url='login')
def main(request):
    user = request.user
    dockerList = Service.objects.filter(user=user)
    username = request.user.username
    idUser = request.user.id
    checkDocker = Service.objects.filter(user=user).exists()
    for docker in dockerList:
        status = checkDeploy(idUser,docker.software,docker.id)
        if status:
            docker.status = True
        else:
            docker.status = False
    context = {'username':username,'dockerList':dockerList,'idUser':idUser,'checkDocker':checkDocker}
    return render(request,'dashboard.html',context)

def userLogout(request):
    logout(request)
    return redirect('../login')

@login_required(login_url='login')
def DeployForm(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            subdomain = form.cleaned_data['subdomain']
            software = form.cleaned_data['software']
            dbpassword = form.cleaned_data['dbpassword']
            user = request.user
            idUser = request.user.id
            try:
                if software == 'mysql' and Service.objects.filter(user_id=idUser, software='mysql').exists():
                    error = "You alredy has a database"
                    return render(request,'form.html',{'form':form,'error':error})
                newService = Service(subdomain=subdomain, software=software,  dbpassword=dbpassword, user=user)
                newService.save()
                idDeploy = newService.id
                if software == 'wp':
                    wordpressManifests(idUser,dbpassword,subdomain,idDeploy)
                    firstStartService(idUser,software,idDeploy)
                if software == 'mysql':
                    mysqlManifests(idUser,dbpassword,idDeploy)
                    phpMyAdminManifests(idUser,dbpassword,subdomain,idDeploy)
                    firstStartService(idUser,software,idDeploy)
                success = "The service was succesfully created 🎉🎉"
                return render(request,'form.html',{'form':form,'success':success})
            except IntegrityError as e :
                print(e)
                error = "Subdomain already exists"
                return render(request,'form.html',{'form':form,'error':error})
    else:
        form = ServiceForm()
    return render(request,'form.html',{'form':form})

def deleteService(request, id):
    deploy = Service.objects.get(id=id)
    deploy.delete()
    return redirect('main')

def newDns(subdomain):
    nsUpdate =f"""
server master.everyhost.io
zone everyhost.io
update add {subdomain}.everyhost.io 300 A 10.43.120.90
send
    """
    process = subprocess.Popen(['nsupdate'], stdin=subprocess.PIPE)
    process.communicate(nsUpdate.encode())
    print(f"Tu url esta lista en: {subdomain}.everyhost.io")

def deleteDns(subdomain):
    nsUpdate =f"""
server master.everyhost.io
zone everyhost.io
update remove {subdomain}.everyhost.io 300 A 10.43.120.90
send
    """
    process = subprocess.Popen(['nsupdate'], stdin=subprocess.PIPE)
    process.communicate(nsUpdate.encode())
    
    
def userDirs(idUser,service,idService):
    if service == "mysql":
       os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/mysql")
       os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/php")
       os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-services/mysql-{idService}")
       os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-services/php-{idService}")
    else:
        os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-services/{service}-{idService}")
        os.makedirs(f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/{service}-{idService}")


def mysqlManifests(idUser,password,idService):
    userDirs(idUser,"mysql",idService)
    dpMysql = kube.mysql(idUser, password,idService)
    pvMysql = kube.servicepv(idUser, "mysql",idService)
    writeManifest(idUser, "mysql", pvMysql, f"mysql-{idUser}-pv.yaml",idService)
    writeManifest(idUser, "mysql", dpMysql, f"mysql-{idUser}-dp.yaml",idService)
    
def nextcloudManifests(idUser,password,subdomain,idService):
    userDirs(idUser,"nc",idService)
    dpNextcloud = kube.nextcloud(idUser, password, idService)
    pvNextcloud = kube.servicepv(idUser, "nextcloud", idService)
    ingressNextcloud = kube.ingress(idUser,subdomain,"nextcloud")
    writeManifest(idUser, "nextcloud", pvNextcloud, f"nextcloud-{idUser}-pv.yaml",idService)
    writeManifest(idUser, "nextcloud", dpNextcloud, f"nextcloud-{idUser}-dp.yaml",idService)
    writeManifest(idUser, "nextcloud", ingressNextcloud, f"nextcloud-{idUser}-ingress.yaml",idService)
    newDns(subdomain)

def wordpressManifests(idUser,password,subdomain,idService):
    userDirs(idUser,"wp",idService)
    dpWordpress = kube.wordpress(idUser, password,idService)
    pvWordpress = kube.servicepv(idUser, "wp",idService)
    ingressWordpress = kube.ingress(idUser,subdomain,"wp",idService)
    writeManifest(idUser, "wp", pvWordpress, f"wp-{idUser}-pv.yaml",idService)
    writeManifest(idUser, "wp", dpWordpress, f"wp-{idUser}-dp.yaml",idService)
    writeManifest(idUser, "wp", ingressWordpress, f"wp-{idUser}-ingress.yaml",idService)
    newDns(subdomain)


def phpMyAdminManifests(idUser,password,subdomain,idService):
    dpPhpMyAdmin = kube.phpMyAdmin(idUser,password,idService)
    ingressPhpMyAdmin = kube.ingress(idUser,subdomain,"php",idService)
    writeManifest(idUser, "php", dpPhpMyAdmin, f"php-{idUser}-dp.yaml",idService)
    writeManifest(idUser, "php", ingressPhpMyAdmin, f"php-{idUser}-ingress.yaml",idService)
    newDns(subdomain)

def writeManifest(idUser, service, manifest, filename,idService):
    if service == "mysql":
        filepath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/{service}/{filename}"
        with open(filepath, "w") as file:
            file.write(manifest)
    elif service == "php":
        filepath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/{service}/{filename}"
        with open(filepath, "w") as file:
            file.write(manifest)
    else:   
        filepath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/{service}-{idService}/{filename}"
        with open(filepath, "w") as file:
            file.write(manifest)

def firstStartService(idUser,service,idService):
    if service == "mysql":
        mysqlPath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/mysql"
        phpPath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/php"
        os.system(f"kubectl apply -f {mysqlPath}")
        os.system(f"kubectl apply -f {phpPath}")
    else:   
        filePath = f"/mnt/nfs/k8s/client-{idUser}/{idUser}-files/{service}-{idService}"
        os.system(f"kubectl apply -f {filePath}")

    
def stopService(request,service,idService):
    idUser = request.user.id
    if service == "mysql":
        deploy = f"client-{idUser}-mysql"
        command = f"kubectl scale deployment {deploy} --replicas=0"
        os.system(command)
        time.sleep(3)
        return redirect('main')
    else:
       deploy= f"client-{idUser}-{service}-{idService}" 
       command = f"kubectl scale deployment {deploy} --replicas=0"
       os.system(command)
       time.sleep(3)
       return redirect('main')
       
    
def startService(request,service,idService):
    idUser = request.user.id
    if service == "mysql":
        deploy = f"client-{idUser}-mysql"
        command = f"kubectl scale deployment {deploy} --replicas=1"
        os.system(command)
        time.sleep(3)
        return redirect('main')
    else:
       deploy= f"client-{idUser}-{service}-{idService}" 
       command = f"kubectl scale deployment {deploy} --replicas=1"
       os.system(command)
       time.sleep(3)
       return redirect('main')
