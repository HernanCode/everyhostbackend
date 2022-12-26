from django.db import models

# Create your models here.


#models.py


#Cada taula es crea amb la seva clau primaria per defecte, no cal afegir-la manualment.


class Users(models.Model):
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField()
    docker = models.ForeignKey('Docker', on_delete=models.CASCADE)


class Web(models.Model):
    path = models.CharField(max_length=100)

class Docker(models.Model):
    web = models.ForeignKey('Web', on_delete=models.CASCADE)
    software = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100)
    port = models.IntegerField()