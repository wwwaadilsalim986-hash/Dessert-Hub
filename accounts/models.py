from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

ROLE_CHOICES= [
    ('baker',"Baker"),
    ('customer',"Customer")
    ] 

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone=models.CharField(max_length=15,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True,blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)



    def __str__(self):
        return f"{self.user.username} - {self.role}"
    

    def is_baker(self):
        return self.role == 'baker'
    
    def is_customer(self):
        return self.role == 'customer'
    



@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)



BUSINESS_TYPE_CHOICES = [
    ('home_baker', 'Home Baker'),
    ('bakery', 'Bakery'),
    ('cloud_kitchen', 'Cloud Kitchen'),
]


class BakerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='baker_profile')
    store_name= models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    banner = models.ImageField(upload_to='banners/', null=True, blank=True)

    phone = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='baker_profiles/', null=True, blank=True)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, null=True, blank=True)
    accepts_custom_orders = models.BooleanField(default=False)

    # Legal Documentation for Bakers
    fssai_number = models.CharField(max_length=20, null=True, blank=True)
    fssai_document = models.ImageField(upload_to='documents/fssai/', null=True, blank=True)
    gst_number = models.CharField(max_length=20, null=True, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    

    # ── Aadhaar ──
    aadhaar_number = models.CharField(max_length=12, null=True, blank=True)
    aadhaar_image_front = models.ImageField(upload_to='documents/aadhaar/', null=True, blank=True)
    aadhaar_image_back = models.ImageField(upload_to='documents/aadhaar/', null=True, blank=True)
    aadhaar_verified = models.BooleanField(default=False)  

    # ── Status ──
    is_verified = models.BooleanField(default=False)  # admin manually verifies
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_name} — {self.user.username}"