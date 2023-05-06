from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
def signup(request):
    if (request.method == 'POST'):
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if (User.objects.filter(email = email).exists() == False) and (User.objects.filter(username = username).exists() == False):
            userdata = User.objects.create_user(username , email , password)
            userdata.save()
            return redirect('/login')
        else:
            return render(request , 'signup.html' , {"message" : "This username is already exist"})
    else:
        return render(request , 'signup.html')