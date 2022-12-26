from django.db import models

# Create your models here.

class Users(models.Model):
    fullname = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    docker = models.ForeignKey('Perfil', on_delete=models.CASCADE)

class Docker(models.Model):
    web = models.ForeignKey('Web', on_delete=models.CASCADE)
    software = models.CharField(max_length=30)
    subdomain = models.CharField(max_length=10)
    docker = models.ForeignKey('Perfil', on_delete=models.CASCADE)
