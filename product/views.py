from django.shortcuts import render , redirect
from django.http import HttpResponse
from products.models import Image , Apertment
from .models import Buyer

def product(request , id):
    if(request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('msg')
        data = Buyer(apertment = id , name = name , email = email , phone = phone , message = message)
        data.save()
        return redirect('sent')
    else:
        global apertment
        apertment = id
        product = Apertment.objects.filter(Apertment_Id = id)
        images = Image.objects.filter(Apertment_Id = id)
        first_image = Image.objects.filter(Apertment_Id = id).first()
        return render(request,'property.html' , {"product" : product , "image":images , "first_image" : first_image})

def buy(request):
    if(request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('msg')
        data = Buyer(apertment = apertment , name = name , email = email , phone = phone , message = message)
        data.save()
        return redirect('sent')
    else:
        return render(request , 'index.html')