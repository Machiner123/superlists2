from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def persona_login(request):
    '''
    1: Instantiate authenticate with data from request as user
    2: If authenticate created user, aka login worked, run login function for user
    '''
    user = authenticate(assertion=request.POST['assertion']) #1
    if user: #2
        login(request, user)
    return HttpResponse('OK')
# Create your views here.
