from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.

def index(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/index.html")
    else:
        return redirect('https://agradehost.com')

def commands(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/commands.html")
    else:
        return redirect('https://agradehost.com')

def tos(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/tos.html")
    else:
        return redirect('https://agradehost.com')

def privacy(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/privacy.html")
    else:
        return redirect('https://agradehost.com')

def changelog(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/changelog.html")
    else:
        return redirect('https://agradehost.com')

def migration(request):

    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/migration.html")
    else:
        return redirect('https://agradehost.com')

def start(request):
    if request.META['HTTP_HOST'] == "mumbobot.xyz":
        return render(request, "frontend/start.html")
    else:
        return redirect('https://agradehost.com')

def invite(request):
    return redirect("https://discord.com/api/oauth2/authorize?client_id=744992005158862939&permissions=8&scope=bot%20applications.commands")
