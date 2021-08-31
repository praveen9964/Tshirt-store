from django.contrib import admin
from store.models import Tshirt,Payment,Order,OrderItem,Cart,Occasion,IdealFor,NeckType,Sleeve,Brand,Color,SizeVariant
from django.utils.html import format_html
# Register your models here.

class SizeVariantConfiguraton(admin.TabularInline):  #this to show size variant model below again 
    model= SizeVariant                               #even stackedInLine is there

class OrderItemConfiguraton(admin.TabularInline): 
    model= OrderItem  



class TshirtConfiguration(admin.ModelAdmin): #which model to display under wch
    inlines=[SizeVariantConfiguraton]   #this is a list show wch model to be displayed\
    list_display =['get_image','name','discount']     #this will show discount in tshirts page in admin site
    list_editable=['discount']
    sortable_by=['name']
    list_filter = ['discount']
    list_per_page=5
    list_display_links=['name']  #if the name of tshirt is clicked it will go to change tshirt page
    # list_editable=['slug'] #this show entry box for slug in  tshirts admin page

    def get_image(self,obj):
        return format_html(f"""
            <a target="_blank" href='{obj.image.url}'><img height="60px" src='{obj.image.url}' /></a>
        
        """)

class CartConfiguration(admin.ModelAdmin): 
    model = Cart   
    #fields=('sizeVariant','quantity','user')
    list_display =['quantity','size','tshirt','user','username']

    fieldsets=(
        ("Cart Info",{"fields":('user','get_tshirt','get_sizeVariant','quantity')}), #in this tshirt function code will be returned
    )
    readonly_fields = ('quantity','user','get_tshirt','get_sizeVariant')    #this fields will be readonly in admin site

    def get_sizeVariant(self,obj):
        return obj.sizeVariant.size

    def get_tshirt(self,obj):
        tshirt=obj.sizeVariant.tshirt 
        tshirt_id= tshirt.id
        name = tshirt.name
        return format_html(f'<a href="/admin/store/tshirt/{tshirt_id}/change/" target="_blank">{name}</a>')
    
    get_tshirt.short_description= 'Tshirt'       #this name will be shown in cart page for a particular product  in admin site
    get_sizeVariant.short_description= 'Size'
    def size(self,obj):
        return obj.sizeVariant.size
    
    def tshirt(self,obj):
        return obj.sizeVariant.tshirt.name
    
    def username(self,obj):
        return obj.user.first_name


class OrderConfiguration(admin.ModelAdmin): 
    #the below comments are for only refernce to know what all attributes are there in Order Table
    #order_status=models.CharField(max_length=15,choices=orderStatus)
    #payment_method=models.CharField(max_length=15,choices=method)
    #shipping_address=models.CharField(max_length=100,null=False)
    #phone=models.CharField(max_length=10,null=False)
    #user=models.ForeignKey(User,on_delete=models.CASCADE)
    #total=models.IntegerField(null=False)
    #date=models.DateTimeField(null=False,auto_now_add=True)  
    list_display =['user','shipping_address','phone','date','order_status']
    readonly_fields=('user',
        'phone',
        'shipping_address',
        'total',
        'payment_method',
        'payment',
        'payment_request_id',
        'payment_id',
        'payment_status')

    fieldsets =(
        ("Order Information",{"fields":('order_status','shipping_address','phone','total','user')}),

        ("payment Information",{"fields":('payment','payment_request_id','payment_id','payment_status')})
    )
    inlines = [OrderItemConfiguraton ]

    def payment_request_id(self,obj):
        return obj.payment_set.all()[0].payment_request_id

    def payment_status(self,obj):
        return obj.payment_set.all()[0].payment_status
    
    def payment_id(self,obj):
        payment_id= obj.payment_set.all()[0].payment_id
        if payment_id is None or payment_id == "":
            return "Payment Id is Not Available"
        else:
            return payment_id
        
    def payment (self,obj):         #obj is current object
        payment_id = obj.payment_set.all()[0].id
        return format_html(f'<a href="/admin/store/payment/{payment_id}/change/" target="_blank">Click For Payment Information</a>')




admin.site.register (Occasion)         #for viiewing Occasion model in admin site
admin.site.register (IdealFor)
admin.site.register (NeckType)
admin.site.register (Sleeve)
admin.site.register (Brand)
admin.site.register (Color)
admin.site.register (Tshirt,TshirtConfiguration)   #this shows sizevariant model below Add Tshirt only
admin.site.register (Cart , CartConfiguration)
admin.site.register (Payment)
admin.site.register (Order , OrderConfiguration)
admin.site.register (OrderItem)
