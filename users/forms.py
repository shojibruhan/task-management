from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tasks.forms import StyleFormMixin


class RegisterForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname ].help_text= None

class CustomRegisterForm(StyleFormMixin, forms.ModelForm):
    password1= forms.CharField(widget= forms.PasswordInput)
    confirmed_password= forms.CharField(widget= forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'confirmed_password']

    def clean_email(self):
         email= self.cleaned_data.get('email')
         email_exist= User.objects.filter(email=email).exists()

         if email_exist:
             raise forms.ValidationError("Email already exists")
    

    def clean_password1(self):  # field error: independent fields
        password1= self.cleaned_data.get('password1')
       
        errors= []

        if len(password1) < 8:
            errors.append("Password must be 8 charecters long.")
        if "abc" not in password1:
            errors.append("Password must contains 'abc")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
    
    
    def clean(self):        # non-field error: two field depend on each others
        cleaned_data= super().clean()
        password1= cleaned_data.get("password1")
        confirmed_password= cleaned_data.get("confirmed_password")

        if password1 != confirmed_password:
            raise forms.ValidationError("Password do not match.")
        
        return cleaned_data


        
        
    