from django import forms
from .models import *


class OrderQuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control auth-input',
            'value': '1',
        })
    )


class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'delivery_name',
            'delivery_phone',
            'delivery_address',
            'delivery_city',
            'delivery_state',
            'delivery_pincode',
            
        ]
        widgets = {
            'delivery_name':    forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'delivery_phone':   forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control auth-input', 'rows': 2}),
            'delivery_city':    forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'delivery_state':   forms.TextInput(attrs={'class': 'form-control auth-input'}),
            'delivery_pincode': forms.TextInput(attrs={'class': 'form-control auth-input'}),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = [
            'delivery_name',
            'delivery_phone',
            'delivery_address',
            'delivery_city',
            'delivery_state',
            'delivery_pincode',
        ]
        for field in required_fields:
            self.fields[field].required = True



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-control auth-input'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control review-textarea',
                'rows': 3,
                'placeholder': 'Share your experience...'
            }),
        }