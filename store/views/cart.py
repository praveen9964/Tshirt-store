from django.shortcuts import render , HttpResponse, redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm   #this is from authforms.py file
from django.contrib.auth.forms import AuthenticationForm  #for built in login form
from django.contrib.auth import authenticate, login as loginUser,logout  #used for login authentication 
                                                #the above authenticate,login and logout are predefined( existing by django)
from store.forms import CheckForm 
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor
from django.contrib.auth.decorators import login_required 

def add_to_cart(request,slug,size):
    user=None
    if request.user.is_authenticated:
        user=request.user
    cart = request.session.get('cart')
    if cart is None:
        cart=[]
    
    tshirt=Tshirt.objects.get(slug=slug)
    add_cart_to_anom_user(cart,size,tshirt)     
           
    if user is not None:
        add_cart_to_database(user,size,tshirt)  
       
    request.session['cart'] = cart  #again inserting into session =cart is a list
    #print( slug, size)
    return_url=request.GET.get('return_url')  #to return to productdetail page again after clicking add to cart
    return redirect(return_url)  #redirecting to the same product page

def add_cart_to_database(user,size,tshirt):
    size=SizeVariant.objects.get(size=size,tshirt = tshirt)
    existing=Cart.objects.filter(user=user,sizeVariant=size)

    if len(existing) > 0:
        obj= existing[0]
        obj.quantity = obj.quantity + 1
        obj.save()        #saving for 
    else:
        c=Cart()           #creating an object for CART Table
        c.user=user           #insert into cart table values for user and below for sizevariant 
        c.sizeVariant=size
        c.quantity=1
        c.save()     #folr saving cart object


def add_cart_to_anom_user(cart,size,tshirt):
    flag = True  
    for cart_obj in cart:
        t_id=cart_obj.get('tshirt')   #will get tshirt id
        size_short=cart_obj.get('size')   #will get size of tshirt

        if t_id == tshirt.id and size == size_short:
            flag=False
            cart_obj['quantity'] = cart_obj['quantity']+1

    if flag:
        cart_obj={
            'tshirt':tshirt.id,
            'size':size,
            'quantity': 1
        }
        cart.append(cart_obj)

def cart(request):
    cart=request.session.get('cart')
    if cart is None:
        cart=[]
    
    for c in cart:
        tshirt_id=c.get('tshirt')        #getting id of tshirt added to cart
        tshirt=Tshirt.objects.get(id=tshirt_id)  #getting data from Tshirt Model
        c['tshirt']=tshirt   #tshirt in dictionary will be updated with tshirt name as a object
        c['size']=SizeVariant.objects.get(tshirt=tshirt_id,size=c['size'])

    print(cart)        
    return render(request , template_name='store/cart.html', context={'cart' : cart})    #to view cart page
