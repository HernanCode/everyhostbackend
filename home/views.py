from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return render(request,'index.html')