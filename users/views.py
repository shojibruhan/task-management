from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from users.forms import CustomRegisterForm, LogInForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator

# def sign_up(request):
#     form= CustomRegisterForm(request.POST or None)
    
#     if request.method == "POST":

        

#         if form.is_valid():
#             # username= form.cleaned_data.get("username")
#             # password= form.cleaned_data.get('password1')
#             # confirmed_password= form.cleaned_data.get('password2')

#             # if password == confirmed_password:
#             #     User.objects.create_user(username= username, password= password)
#             user= form.save(commit= False)
#             print("user", user)
#             user.email= form.cleaned_data.get('email')
#             user.set_password(form.cleaned_data.get("password1"))

#             print(form.cleaned_data)
#             user.is_active= False
#             user.save()
#             messages.success(request, "Activate your account. Link sent to your email.")
#             return redirect('sign-in')
#         else:
#             print("Form is not valid.")
            
            
#     return render(request, "registration/register.html", {"form":form})

def sign_up(request):
    form = CustomRegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data.get("email")  # Ensure email is explicitly set
        user.set_password(form.cleaned_data.get("password1"))
        user.is_active = False
        user.save()
        messages.success(request, "Activate your account. Link sent to your email.")
        return redirect('sign-in')

    return render(request, "registration/register.html", {"form": form})


def sign_in(request):
    
    form= LogInForm()

    if request.method== "POST":
        form= LogInForm(data= request.POST)
        if form.is_valid():
            user= form.get_user()
            login(request, user)
            return redirect('home')
   
    return render(request, "registration/login.html", {"form":form})

def sign_out(request):
     if request.method == "POST":
        logout(request)
        return redirect("sign-in")
     
def activate_user(request, user_id, token):
    try:
        user= User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active= True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid ID or Token")
    except:
        return HttpResponse("No User found!")
