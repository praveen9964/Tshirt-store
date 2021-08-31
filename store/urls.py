
from django.contrib import admin
from django.urls import path
from store.views import home,cart,LoginView,OrderListView, signout,signup,add_to_cart,checkout ,contact_us
from store.views import validatePayment ,ProductDetailView
from django.contrib.auth.decorators import login_required 


urlpatterns = [
    path('',home,name='homepage'),   #here name is alias
    path('cart/',cart),     #to view cart page , 2nd cart is a function created in views.py in store folder 
    path('orders/',login_required(OrderListView.as_view(),login_url='/login'),name='orders'),
    path('login/',LoginView.as_view(), name='login'),
    path('signup/',signup),
    path('logout/',signout),
    path('checkout/',checkout),
    path('product/<str:slug>',ProductDetailView.as_view()),
    path('addtocart/<str:slug>/<str:size>',add_to_cart),
    path('validate_payment/',validatePayment),
    path('contactus/',contact_us),

    
   
]
