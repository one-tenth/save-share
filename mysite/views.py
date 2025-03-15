from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("hello world")

def indexhome(request):
    return render(request, 'indexhome.html')