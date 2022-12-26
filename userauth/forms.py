from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma la contraseña',widget=forms.PasswordInput)
    class Meta: 
        model = User
        fields = ['username', 'email', 'password1','password2']
        help_texts = {k: "" for k in fields} # Iteramos en cada uno de los strings de helptext para dejarlo en blanco