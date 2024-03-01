from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'layouts/index.html')

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save()
        
        messages.info(request, 'Account created')
        return redirect('/dashboard/')
   
    return render(request, 'auth/register.html')

def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, 'Invalid Username ')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.info(request, 'Invalid Password ')
            return redirect('/login/')  

        else:
            login(request,user)
            return redirect('dashboard')  
    return render(request, 'auth/login.html')

@login_required(login_url='login')
def dashboard_view(request):
    return render(request,'layouts/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('home')
