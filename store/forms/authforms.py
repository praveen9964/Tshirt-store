from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User    #importing model for form
from django.core.exceptions import ValidationError

class CustomerAuthForm(AuthenticationForm):
    username=forms.EmailField(required=True, label="Email")

class CustomerCreationForm(UserCreationForm):
    username=forms.EmailField(required=True, label="Email")
    first_name=forms.CharField(required=True, label="First Name") #first_name should be same as it is predefined
    last_name=forms.CharField(required=True, label="Last Name")

    def clean_first_name(self):          #this is for validation ,it ll be internally called automatically
        value=self.cleaned_data.get('first_name')       #first time will be stored in value
        if len(value.strip())<4:
            raise ValidationError("First Name must be 4 Char Long")  #this will be shown in site
        return value.strip()
    
    def clean_last_name(self):        #clean_(here form fields) 
        value=self.cleaned_data.get('last_name')       
        if len(value.strip())<4:
            raise ValidationError("Last Name must be 4 Char Long")  
        return value.strip()
    
    

    class Meta:     #to display
        model = User       #this form for wch model
        fields=['username','first_name','last_name']