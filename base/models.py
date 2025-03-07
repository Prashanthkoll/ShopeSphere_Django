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


class Address(models.Model):
    host= models.ForeignKey(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    phone= models.IntegerField(default='00000000')
    house= models.TextField()
    street= models.TextField()
    land= models.TextField()
    city= models.CharField(max_length=100)
    state= models.CharField(max_length=100)
    pincode= models.IntegerField(default='0000')
    country= models.CharField(max_length=100, default="India")
    instructions= models.TextField(blank=True, null=True)

class Delivery(models.Model):
    shop_upi=models.IntegerField(default=2)
    upi=models.IntegerField(default=3)
    shop_balance=models.IntegerField(default=2)
    net_bank=models.IntegerField(default=3)
    cash_on=models.IntegerField(default=7)
    Free=models.IntegerField(default=0)
    Oneday=models.IntegerField(default=79)

