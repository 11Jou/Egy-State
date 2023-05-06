from django.shortcuts import render , redirect
from .models import Message
# Create your views here.

def index(request):
    if(request.method == 'POST'):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('msg')
        data = Message(name = name , email = email , phone = phone , message = message)
        data.save()
        return redirect('sent')
    else:
        return render(request , 'index.html')
    

def send(request):
    return render(request , 'send.html')