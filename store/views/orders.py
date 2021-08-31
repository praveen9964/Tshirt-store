from django.shortcuts import render , HttpResponse, redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm   #this is from authforms.py file
from django.contrib.auth.forms import AuthenticationForm  #for built in login form
from django.contrib.auth import authenticate, login as loginUser,logout  #used for login authentication 
                                                #the above authenticate,login and logout are predefined( existing by django)
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor

from django.views.generic.list import ListView

# @login_required(login_url='/login') 


class OrderListView(ListView):
    template_name="store/orders.html"
    paginate_by=5
    model = Order
    
    context_object_name='orders'


    def get_queryset(self):
        print("GET QUERY SET")
        print()
        return Order.objects.filter(user = self.request.user).order_by('-date').exclude(order_status='PENDING') #we will get in descending order
