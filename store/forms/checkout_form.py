from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User    #importing model for form
from django.core.exceptions import ValidationError
from store.models import Order



class CheckForm(forms.ModelForm):
    class Meta:        #this means for wch model this form is used
        model = Order
        fields = ['shipping_address','phone','payment_method']   #only the specified attribute will be shown as form 