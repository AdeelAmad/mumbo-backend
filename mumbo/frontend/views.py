from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    print(request.META['HTTP_HOST'])
    # if request.META['HTTP_HOST'] == "mumbobot.xyz":
    #     return HttpResponse(status=200)
    # else:
    #     return redirect('https://mumbobot.xyz')

def commands(request):
    print(request.META['HTTP_HOST'])
    # if request.META['HTTP_HOST'] == "mumbobot.xyz":
    #     return HttpResponse(status=200)
    # else:
    #     return redirect('https://mumbobot.xyz')

def tos(request):
    print(request.META['HTTP_HOST'])
    # if request.META['HTTP_HOST'] == "mumbobot.xyz":
    #     return HttpResponse(status=200)
    # else:
    #     return redirect('https://mumbobot.xyz')

def privacy(request):
    print(request.META['HTTP_HOST'])
    # if request.META['HTTP_HOST'] == "mumbobot.xyz":
    #     return HttpResponse(status=200)
    # else:
    #     return redirect('https://mumbobot.xyz')