from django.shortcuts import render , HttpResponse, redirect
from store.forms.authforms import CustomerCreationForm,CustomerAuthForm   #this is from authforms.py file
from django.contrib.auth import authenticate, login as loginUser,logout  #used for login authentication 
                                                #the above authenticate,login and logout are predefined( existing by django)
from store.forms import CheckForm ,CustomerCreationForm, CustomerAuthForm
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from django.views.generic.base import View

class LoginView(View):       #now LoginView is class
    print("LOGIN VIEW CLASS")
    def get(self,request):         #this will handle GET request
        form=CustomerAuthForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page
        return render(request,template_name="store/login.html",context={ 'form':form})

    def post(self,request): #this will handle POST request
        form=CustomerAuthForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user:
                loginUser(request,user)  #if this is not given it shows anaonymous user

                session_cart = request.session.get('cart')   #to merge before login cart items to after login
                if session_cart is None:
                    session_cart=[]
                else:
                    for c in session_cart:
                        size=c.get('size')
                        tshirt_id=c.get('tshirt')
                        quantity=c.get('quantity')
                        cart_obj=Cart()           #creating new object for Cart Model
                        cart_obj.sizeVariant = SizeVariant.objects.get(size=size,tshirt =tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user=user
                        cart_obj.save()

                # { size , tshirt,quantity}
                cart = Cart.objects.filter(user=user)
                session_cart=[]
                for c in cart:
                    obj={
                        'size':c.sizeVariant.size,
                        'tshirt' : c.sizeVariant.tshirt.id,
                        'quantity': c.quantity
                    }
                    session_cart.append(obj)
                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is  None:
                    next_page='homepage'
                return redirect(next_page)
        else:
            return render(request,template_name="store/login.html",context={ 'form':form})
        
       

def signout(request): 
    logout(request)    #request.session.clear() this also can be written to clear session object of user when logged out
    return render(request,template_name="store/home.html")

def signup(request):
    if (request.method == 'GET'):        
        form=CustomerCreationForm()
        context={
            "form":form
        }
        return render(request,template_name="store/signup.html",context=context)
    else:
        form=CustomerCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.email = user.username
            user.first_name=user.first_name
            user.save()
            return redirect ('login')
            
        context={
            "form":form
        }
        return render(request,template_name="store/signup.html",context=context)
