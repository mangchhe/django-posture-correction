from django.db import models

# Create your models here.

class User(models.Model):
    user_ID = models.CharField(max_length = 50)
    user_password = models.CharField(max_length = 50)
    user_name = models.CharField(max_length = 50)
    user_birth = models.DateField()
