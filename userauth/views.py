from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
import os


# Create your views here.
def home(request):
    return render(request,'home.html')


def bar(request):
    return render(request,'bar.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('../dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('../dashboard')
            else:
                messages.info(request, 'El usuario o la contraseña no son correctos')
        return render(request,'login.html')

def error_404(request, exception):
    return render(request, '404.html')

def signupPage(request):
    if request.user.is_authenticated:
        return redirect('../dashboard')
    else:
        form = UserRegisterForm()
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Cuenta ' + user + ' creada correctamente')
                os.makedirs(f'/home/samuel/hostingfolders/{user}')
                return redirect('login')
            else:
                messages.info(request, 'La contraseña con cumple con la complejidad necesaria o el usuario ya esta en uso')

    context = {'form':form}
    return render(request, 'signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')



