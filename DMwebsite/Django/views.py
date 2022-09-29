from django.http import HttpResponse
from django.shortcuts import render
def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')

def about(request):
   # return HttpResponse('about')
   return render(request, 'about.html')

def signup(request):
    return render(request, 'authentication/signup.html')

def signin(request):
    return render(request, 'authentication/signin.html')

def signout(request):
    pass

