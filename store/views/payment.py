from django.shortcuts import render , HttpResponse, redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm   #this is from authforms.py file
from django.contrib.auth.forms import AuthenticationForm  #for built in login form
from django.contrib.auth import authenticate, login as loginUser,logout  #used for login authentication 
                                                #the above authenticate,login and logout are predefined( existing by django)
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor
from django.contrib.auth.decorators import login_required    #this is for when a user without login clicks checkout then login page should be shown
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY, AUTH_TOKEN

API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')


            
def validatePayment(request):
    user = None
    if request.user.is_authenticated :
        user = request.user
    print(user)
    payment_request_id = request.GET.get ('payment_request_id')
    payment_id= request.GET.get('payment_id')
    #below is checking or validating payment
    response = API.payment_request_payment_status(payment_request_id,payment_id)
    #print response['payment_request']['purpose']             # Purpose of Payment Request
    status = response.get('payment_request').get('payment').get('status')  # Payment status   #get is used bcoz it is dictionary and it will return None if ift is not found
    print (status)  
    if status != "Failed":
        print ('Payment Success')
        try:
            payment = Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status= status
            payment.save()

            order = payment.order
            order.order_status = 'PLACED'
            order.save()

            #the below 2lines is to clear the cart after the order is placed
            cart = []
            request.session['cart'] = cart

            #below code is to delete cart data from the database for a particular user
            Cart.objects.filter(user = user ).delete()


            return redirect ('orders')  #this will redirect to orders page 
        except:
            return render(request,'store/payment_failed.html')

    else:
        #return error page
        return render(request,'store/payment_failed.html')
