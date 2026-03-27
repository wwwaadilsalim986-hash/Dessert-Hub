from django import forms
from django.contrib.auth.models import User
from .models import *


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'is_available', 'stock',]