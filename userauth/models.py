from django.db import models

# Create your models here.


#models.py


#Cada taula es crea amb la seva clau primaria per defecte, no cal afegir-la manualment.


class Users(models.Model):
    fullname = models.CharField()
    password = models.CharField()
    email = models.EmailField()
    docker = models.ForeignKey('Perfil', on_delete=models.CASCADE)

class Docker(models.Model):
    web = models.ForeignKey('Web', on_delete=models.CASCADE)
    software = models.CharField()
    subdomain = models.CharField()
    port = models.IntegerField(max_length=5)

class Web(models.Model):
    path = models.CharField()