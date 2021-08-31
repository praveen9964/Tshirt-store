from django.shortcuts import render , HttpResponse, redirect

#this is for contact us page
def contact_us(request):
    return render(request,template_name="store/contactus.html")
