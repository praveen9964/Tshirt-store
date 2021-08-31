from store.views.home import home   #in the store folder ,then inside views folder and inside that home.py file we are importing home function
from store.views.cart import cart,add_to_cart   #cart is main view function and others in cart.py are for utility
from store.views.checkout import checkout
from store.views.orders import  OrderListView
from store.views.payment import validatePayment
from store.views.product_page import ProductDetailView
from store.views.authentication import LoginView, signout , signup
from store.views.contactus import contact_us