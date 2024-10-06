from django.db import models
from datetime import datetime

# Create your models here.
class Carousal(models.Model):
    image = models.ImageField(upload_to='products/')

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    specification = models.TextField()

class Customer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=200)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=300)
    date = models.DateField(default=datetime.today())
    completed = models.BooleanField(default=False)
