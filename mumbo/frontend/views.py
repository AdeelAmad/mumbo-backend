from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    print(request.META['HTTP_HOST'])


    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/index.html")
    else:
        return redirect('https://mumbobot.xyz')

def commands(request):
    print(request.META['HTTP_HOST'])


    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/commands.html")
    else:
        return redirect('https://mumbobot.xyz')

def tos(request):
    print(request.META['HTTP_HOST'])


    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/tos.html")
    else:
        return redirect('https://mumbobot.xyz')

def privacy(request):
    print(request.META['HTTP_HOST'])


    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/privacy.html")
    else:
        return redirect('https://mumbobot.xyz')

def changelog(request):
    print(request.META['HTTP_HOST'])


    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/changelog.html")
    else:
        return redirect('https://mumbobot.xyz')