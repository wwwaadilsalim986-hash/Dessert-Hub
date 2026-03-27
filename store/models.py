from django.db import models

from django.contrib.auth.models import User

from accounts.models import BakerProfile

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import *

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='Category', null=True,blank=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
     baker=models.ForeignKey(User,on_delete=models.CASCADE)
     category=models.ForeignKey(Category,on_delete=models.CASCADE)

     name=models.CharField(max_length=100)
     description=models.TextField()
     price=models.DecimalField(max_digits=10,decimal_places=2)

     stock=models.PositiveIntegerField()

     created_at=models.DateTimeField(auto_now_add=True)
     updated_at=models.DateTimeField(auto_now_add=True)

     is_available=models.BooleanField(default=True)

     def __str__(self):
         return self.name
     

class ProductImage(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='product_images/')

    def __str__(self):
         return f"image for {self.product.name}"
       




