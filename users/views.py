from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from users.forms import CustomRegisterForm

def sign_up(request):
    form= CustomRegisterForm()
    
    if request.method == "POST":
        form= CustomRegisterForm(request.POST)

        if form.is_valid():
            # username= form.cleaned_data.get("username")
            # password= form.cleaned_data.get('password1')
            # confirmed_password= form.cleaned_data.get('password2')

            # if password == confirmed_password:
            #     User.objects.create_user(username= username, password= password)
                form.save()
        else:
            print("Form is not valid.")
            
            
    return render(request, "registration/register.html", {"form":form})

def sign_in(request):
    if request.method== "POST":
        username= request.POST.get("username")
        password= request.POST.get("password")
        print("info:", username, password)
        user= authenticate(request, username=username, password= password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('home')

   
    return render(request, "registration/login.html")

def sign_out(request):
     if request.method == "POST":
        logout(request)
        return redirect("sign-in")