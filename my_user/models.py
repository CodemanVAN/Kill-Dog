from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# Create your models here.
class User(AbstractUser):
    userHost=models.CharField(max_length=30)
    userLevel=models.IntegerField(default=1)
    userAnalyzeNum=models.IntegerField(default=10)
    userBoss=models.CharField(max_length=255)
    userIsSubicated=models.BooleanField(default=False)
    
class History(models.Model):
    userName=models.CharField(max_length=30)
    recordMatchid=models.CharField(max_length=10)
    recordHostteam=models.CharField(max_length=255)
    recordAwayteam=models.CharField(max_length=255)
    recordPredict=models.CharField(max_length=10)
    rcecordPan=models.CharField(max_length=10)
    recordResult=models.CharField(max_length=10)
    recordTime=models.DateTimeField(default=datetime.now)

