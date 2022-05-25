from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password1 == password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register') 
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user= User.objects.create_user(username=username,password=password,email=email)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'passwords not matching')
            return redirect('register')
        
    else:
        return render(request,'register.html')
def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        userinfo= User.objects.filter(email=email)
        if userinfo.exists():
            username=userinfo.first()
        else:
            messages.info(request,'Email doesn\'t exist..')
            return redirect('login')

        password=request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid credentials. Enter correct password')
            return redirect('login')
    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('index')