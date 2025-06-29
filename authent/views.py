from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def Register(request):
    log_nav=True
    if request.method=="POST":
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        user=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        a=User.objects.filter(username=user).first()
        if not a:
            User.objects.create(username=user,email=email,password=password,last_name=last_name,first_name=first_name)
            return redirect('login')
        else:
            messages.error(request,'User is existed Already.')
    return render(request,'register.html',{'log_nav':log_nav})
def Login(request):
    log_nav=True
    if request.method=="POST":
        user=request.POST['name']
        password=request.POST['password']
        usernames=[]
        a=User.objects.all()
        for i in a:
            usernames+=[i.username]
        if user in usernames:
            data=User.objects.get(username=user)
            if data.password==password:
                login(request,data)
                return redirect('home')
            else:
                messages.error(request,'Password is incorrect!, Try Again.')
        else:
            messages.error(request,'Username is not found!, Try Again.')
    return render(request,'login.html',{'log_nav':log_nav})



@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login') 


@login_required(login_url='login')
def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    else:
        return render(request,'login.html')

@login_required(login_url='login')
def editprofile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST['firstname']
        request.user.last_name = request.POST['lastname']
        request.user.username = request.POST['name']
        request.user.email = request.POST['email']
        request.user.save()
        return redirect('profile')
    messages.success(request, "Profile updated successfully.")
    return render(request, 'editprofile.html')



@login_required(login_url='login')
def changepassword(request):
    if request.method == 'POST':
        oldpassword=request.POST['oldpassword']
        newpassword=request.POST['newpassword']
        if request.user.password==oldpassword:
            request.user.password=newpassword
            request.user.save()
            return redirect('login')
        else:
            messages.error(request, "Old Password in not matchet, Try Again.")
    return render(request, 'changepassword.html')
