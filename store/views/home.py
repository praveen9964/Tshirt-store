from django.shortcuts import render , HttpResponse, redirect
from store.models import Tshirt,SizeVariant, Cart , Order , OrderItem , Payment, Occasion,IdealFor,NeckType,Sleeve,Brand,Color 
from django.core.paginator import Paginator
from urllib.parse import urlencode



def home(request):
    #getting what is selected like brand ,color from the url using GET 
    query=request.GET
    tshirts=[]
    tshirts= Tshirt.objects.all()
    brand = query.get('brand')   #since query is of dictionary type get is used
    neckType = query.get('necktype')
    color = query.get('color')
    idealFor = query.get('idealfor')
    sleeve = query.get('sleeve')
    page=query.get('page')

    if page is  None or page =="":
        page=1


    if brand != '' and brand is not None:
        tshirts = tshirts.filter(brand__slug=brand) #brand _ _ slug meaning referreing in tshirt table brand attribute which is foreign  key and referrning slug from brand table
    if neckType !='' and neckType is not None:
        tshirts = tshirts.filter(neck_type__slug=neckType)
    if color !='' and color is not None:
        tshirts = tshirts.filter(color__slug=color)
    if idealFor !='' and idealFor is not None:
        tshirts = tshirts.filter(ideal_for__slug=idealFor)
    if sleeve !='' and sleeve is not None:
        tshirts = tshirts.filter(sleeve__slug=sleeve)
    
    #tshirts=Tshirt.objects.filter(brand__slug = brand)   #to get all the Tshirt Objects with objectname as title of tshirt
    occasions = Occasion.objects.all()
    idealFor= IdealFor.objects.all()
    neckTypes= NeckType.objects.all()
    sleeves= Sleeve.objects.all()
    brands= Brand.objects.all()
    colors= Color.objects.all()

    #print(tshirts)
    #print(len(tshirts))    
    cart = request.session.get('cart')
    #print(cart)

    paginator = Paginator(tshirts,3)         #for viewing limited products in a page
    page_object = paginator.get_page(page)  #we will get all details in page_object like how many pages are there ,next page etc

    query = request.GET.copy()
    query['page']=""  #inserting a new key 'page' and value is ""
    pageurl = urlencode(query)        #urllencode is used to get the url as a string and not as dictionary

    context={
        "page_object":page_object,
        "occasions":occasions,
        "idealFor":idealFor ,
        "neckTypes":neckTypes,
        "sleeves":sleeves,
        "brands":brands,
        "colors":colors,
        "pageurl":pageurl

    }
    return render(request,template_name="store/home.html",context=context)  #context is for printing data
