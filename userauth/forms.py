from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm your password',widget=forms.PasswordInput)
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1','password2']
        help_texts = {k: "" for k in fields} # Iteramos en cada uno de los strings de helptext para dejarlo en blanco