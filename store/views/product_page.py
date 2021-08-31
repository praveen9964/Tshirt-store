from django.shortcuts import render , HttpResponse, redirect
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color
from math import floor
from django.views.generic.detail import DetailView

class ProductDetailView(DetailView):
    template_name="store/product_details.html"
    model = Tshirt

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)   #keyword args will provide a slug for Tshirt Model to extract context
        tshirt = context.get('tshirt')
        request = self.request
        size=request.GET.get('size')   #we will get the size selected by user
        if size is None:
            size=tshirt.sizevariant_set.all().order_by('price').first()  #by default to display tshirt with  less cost for a size
        else:
            size=tshirt.sizevariant_set.get(size=size) #if user click size then to show that price
        size_price= floor(size.price)
        sell_price=size_price - (size_price*(tshirt.discount/100))
        sell_price=floor(sell_price)
        print(size)
        context={'tshirt':tshirt,
        'price' : size_price,
        'sell_price':sell_price,
        'active_size':size}
        return context

def show_product(request,slug):

    return render(request,context=context)
