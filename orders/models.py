from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.


class Order(models.Model):
    order_status_choices = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),

    ]

    customer=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity=models.PositiveIntegerField()
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20, choices=order_status_choices, default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    

    # Delivery details
    delivery_name = models.CharField(max_length=100, blank=True)
    delivery_phone = models.CharField(max_length=15, blank=True)
    delivery_address = models.TextField(blank=True)
    delivery_city = models.CharField(max_length=100, blank=True)
    delivery_state = models.CharField(max_length=100, blank=True)
    delivery_pincode = models.CharField(max_length=10, blank=True)
    

    def __str__(self):
        return f"order #{self.id} by {self.customer.username}"
    





class Review(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveIntegerField(default=5)
    created_at=models.DateTimeField(auto_now_add=True)  
    comment=models.TextField(blank=True)

    def __str__(self):
        return f"Review by {self.customer.username} on {self.product.name}"
    

