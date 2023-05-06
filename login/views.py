from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
# Create your views here.

def signin(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)
        if user is not None:
            login(request , user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'msg':"Username or Password is Wrong !"})
    else:
        return render(request, 'login.html')
    
def signout(request):
    logout(request)
    return redirect('/')