from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    category=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    img=models.ImageField(default='default.png',upload_to='uploads')
    sale=models.BooleanField(default=False)
    trending=models.BooleanField(default=False)

class AddCard(models.Model):
    category=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    img=models.ImageField(default='default.png',upload_to='uploads')
    host=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    quantity=models.PositiveIntegerField(default=1)
    totalprice=models.IntegerField(default=0)

class Buy(models.Model):
    category=models.CharField(max_length=300)
    name=models.CharField(max_length=300)
    desc=models.CharField(max_length=1000)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    img=models.ImageField(default='default.png',upload_to='uploads')
    host=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    quantity=models.PositiveIntegerField(default=1)
    totalprice=models.IntegerField(default=0)
    