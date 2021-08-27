from django.db import models

# Create your models here.

class Tenants(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)