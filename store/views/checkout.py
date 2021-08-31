from django.shortcuts import render , HttpResponse, redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm   #this is from authforms.py file
from django.contrib.auth.forms import AuthenticationForm  #for built in login form
from store.forms import CheckForm ,CustomerCreationForm, CustomerAuthForm
from django.contrib.auth import authenticate, login as loginUser,logout  #used for login authentication 
                                                #the above authenticate,login and logout are predefined( existing by django)
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor
from django.contrib.auth.decorators import login_required 
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY, AUTH_TOKEN

API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/') #now in production Mode



       
#just for utility
def cal_total_payable_amount(cart):         #for adding total amount in cart page 
    total=0
    for c in cart:
        discount=c.get('tshirt').discount
        price=c.get('size').price
        sale_price=floor(price- (price*(discount/100)))
        total_of_single_product=sale_price *  c.get('quantity')
        total=total + total_of_single_product

    return total


@login_required(login_url='/login')   #it is a decorator
def checkout(request):
    if request.method == 'GET':     #for get Request
        form = CheckForm()
        cart=request.session.get('cart')
        if cart is None:
            cart=[]
        
        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj=SizeVariant.objects.get(size=size_str , tshirt=tshirt_id)   #now in cart list ,size is replaced by its object
            c['size']=size_obj
            c['tshirt']=size_obj.tshirt   #replacing in cart list , tshirt is id ,inplace of id tshirt object is stored

        return render(request,'store/checkout.html',{"form" : form, 'cart':cart})
    else:
        #this is for POST request
        form = CheckForm(request.POST)
        user = None
        if request.user.is_authenticated :
            user = request.user
        if form.is_valid():
            #payment should be done here
            cart=request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj=SizeVariant.objects.get(size=size_str , tshirt=tshirt_id)   #now in cart list ,size is replaced by its object
                c['size']=size_obj
                c['tshirt']=size_obj.tshirt
            shipping_address=form.cleaned_data.get('shipping_address')   #the shipping address entered will be stored in shipping_address variable
            phone=form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_payable_amount(cart)
            print(shipping_address,phone,payment_method , total)
            order= Order()               #created Order Model object
            order.shipping_address = shipping_address   #entering data in ORDER table
            order.phone = phone
            order.payment_method= payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()    
            #print(order.id)        # we will get order id 

            #saving to OrderItems Table
            for c in cart :
                order_item = OrderItem()   #creating new object for OrderItem Table
                order_item.order = order      #order id will be stored in order
                size=c.get('size')   #to access dictionary we use get('key')
                tshirt=c.get('tshirt')
                order_item.price = floor(size.price- (size.price*(tshirt.discount/100)))
                order_item.quantity = c.get('quantity')
                order_item.size = size
                order_item.tshirt = tshirt
                order_item.save()

            
            # CREATING PAYMENT
            # Create a new Payment Request
            response = API.payment_request_create(
                amount=order.total,
                purpose='Payment For Tshirts',
                buyer_name=f'{user.first_name} {user.last_name}',
                send_email=True,
                email=user.email,
                redirect_url="http://localhost:8000/validate_payment"
                )
            #print(response['payment_request'])
            payment_request_id = response['payment_request']['id']
            #the long URL of the payment request
            url =response['payment_request']['longurl']
            print(url)
            
            payment= Payment()
            payment.order= order
            payment.payment_request_id= payment_request_id
            payment.save()
            return redirect(url)
        else:
            return redirect('/checkout/')
