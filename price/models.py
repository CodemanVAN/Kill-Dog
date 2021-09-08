from django.db import models

# Create your models here.
class Addkeys(models.Model):
    userName=models.CharField(max_length=30,default=None,blank=True)
    keyString=models.CharField(max_length=255)
    usedTime=models.DateTimeField(default=None,blank=True)