from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from users.forms import CustomRegisterForm, LogInForm, AssigneRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch



# Test for user

def is_admin(user):
    return user.groups.filter(name= "Admin").exists()
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

@login_required
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



@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users= User.objects.prefetch_related(
        Prefetch('groups',
                 queryset=Group.objects.all(),
                 to_attr='all_groups')
        
    ).all()
    
    for user in users:
        if user.all_groups:
            user.group_name= user.all_groups[0].name
        else:
            user.group_name= "No Group Assigned"

    context= { 
        "users": users
    }
    return render(request, "admin/dashboard.html", context)


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    user= User.objects.get(id= user_id)
    form= AssigneRoleForm()
    if request.method== "POST":
        form= AssigneRoleForm(request.POST)
        if form.is_valid():
            role= form.cleaned_data.get("role")
            user.groups.clear() # Remove old roles
            user.groups.add(role)
            messages.success(request, f"{user.username} has been assigned to the {role.name} role.")
            return redirect('dashboard')
    return render(request, "admin/assign_role.html", {"form":form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form= CreateGroupForm()
    if request.method == "POST":
        form= CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"{group.name} has benn created successfully")
            return redirect("create-group")
    return render(request, "admin/create_group.html", {"form": form})
    
    
def group_list(request):
    groups= Group.objects.prefetch_related('permissions').all()

    return render(request, "admin/group_list.html", {"groups": groups})
    
