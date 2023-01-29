from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Docker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    software = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100)
    port = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    repository=models.CharField(max_length=100)
    dbadmin=models.CharField(max_length=100)
    dbpassword=models.CharField(max_length=228)