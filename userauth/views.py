from django.shortcuts import render,redirect
from .models import * 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm

# Create your views here.

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('/auth/dashboard')
        else:
            messages.info(request, 'El usuario o la contraseña no son correctos')
    context = {}
    return render(request,'login.html',context)

def signupPage(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Cuenta ' + user + ' creada correctamente')
            return redirect('/auth/login')
    context = {'form':form}
    return render(request, 'signup.html', context)

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

def dashboard(request):
    return render(request,'dashboard.html')

