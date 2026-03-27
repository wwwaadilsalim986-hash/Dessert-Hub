from django import forms
from django.contrib.auth.models import User
from .models import *


class RegisterForm(forms.Form):
    username=forms.CharField(max_length=100)
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)


class CustomerProfileForm(forms.ModelForm):
         class Meta:
                model=UserProfile
                fields=['phone','address','city','state','pincode','profile_pic']



class BecomeBakerForm(forms.ModelForm):
    class Meta:
        model = BakerProfile
        fields = [
            'store_name',
            'description',
            'banner',

            'phone',
            'city',
            'state',
            'profile_pic',

            'business_type',
            'years_of_experience',
            'accepts_custom_orders',

            'fssai_number',
            'fssai_document',
            'gst_number',

            'aadhaar_number',
            'aadhaar_image_front',
            'aadhaar_image_back',
        ]

 
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['store_name', 'description', 'banner', 'phone','city','state', 'business_type','aadhaar_number', ]
        for field in required_fields:
                self.fields[field].required=True


       
