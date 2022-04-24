import json
import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Guild
import sys
sys.path.append('../mumbo')


@csrf_exempt
def index(request):
    # GET to retrieve data
    if request.method == "GET":
        body = json.loads(request.body)
        # Check if guild object exists for guild
        if Guild.objects.filter(id=body['id']):
            g = Guild.objects.get(id=body['id'])

            response = {
                "id": g.id,
                "counting": g.counting,
                "voicechannel": g.voicechannel,
                "leveling": g.leveling,
                "afkmusic": g.afkmusic,
                "alert": g.alert
            }

            return JsonResponse(data=response, status=200)
        # Return 404 if object not exist
        return HttpResponse(status=404)


    # Post to create guild object if 404 returned from GET method or on server join
    elif request.method == "POST":
        body = json.loads(request.body)
        # If guild object exists
        if Guild.objects.filter(id=body['id']):
            # would create conflict to have two guild objects
            return HttpResponse(status=409)
        else:
            # Create the guild object
            guild = Guild(id=body['id'])
            # Save the guild object
            guild.save()

            # Create all sub objects
            guild.count_set.create()


            return HttpResponse(status=200)


    # PATCH to update data
    elif request.method == "PUT":
        body = json.loads(request.body)
        if Guild.objects.filter(id=body['id']):
            g = Guild.objects.get(id=body['id'])
            g.counting = body['counting']
            g.voicechannel = body['voicechannel']
            g.leveling = body['leveling']
            g.afkmusic = body['afkmusic']
            g.alert = body['alert']
            g.save()
            response = {
                "id": g.id,
                "counting": g.counting,
                "voicechannel": g.voicechannel,
                "leveling": g.leveling,
                "afkmusic": g.afkmusic,
                "alert": g.alert
            }
            return JsonResponse(data=response, status=200)
        else:
            # Return 404 if object not exist
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)