from django.http import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login,
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

def loginView(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
        else:
            return render('login.html', context_instance=RequestContext(request))

def logoutView(request):
    pass

def registerView(request):
    return render(request,'store/base.html')

    