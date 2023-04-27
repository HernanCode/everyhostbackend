from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    software = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    dbadmin=models.CharField(max_length=100)
    dbpassword=models.CharField(max_length=228)
    replicas=models.CharField(max_length=5)
    hasMysql = models.BooleanField(default=False)
    