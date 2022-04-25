import json
import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import voicechannelsetting
import sys
sys.path.append('../mumbo')

from management.models import Guild

@csrf_exempt
def index(request):
    # GET to retrieve data
    if request.method == "GET":
        body = json.loads(request.body)
        # Check if guild object exists for guild
        if voicechannelsetting.objects.filter(guild_id=body['id']):

            v = voicechannelsetting.objects.get(guild_id=body['id'])

            response = {
                "guild_id": int(v.guild_id.id),
                "channel_id": int(v.channel_id),
                "category": int(v.category),
                "bitrate": v.bitrate
            }

            return JsonResponse(data=response, status=200)
        # Return 404 if object not exist
        return HttpResponse(status=404)


    # Post to create guild object if 404 returned from GET method or on server join
    elif request.method == "POST":
        body = json.loads(request.body)
        print(body)
        # If guild object exists
        if voicechannelsetting.objects.filter(guild_id=body['id']):
            # would create conflict to have two guild objects
            return HttpResponse(status=409)
        else:
            # Get the Guild object
            guild = Guild.objects.get(pk=body['id'])

            # Create voicechannelsetting object w/ guild foreign key
            guild.voicechannelsetting_set.create()

            return HttpResponse(status=200)


    # PATCH to update data
    elif request.method == "PUT":
        body = json.loads(request.body)
        if voicechannelsetting.objects.filter(guild_id=body['id']):
            v = voicechannelsetting.objects.get(guild_id=body['id'])
            v.channel_id = body['channel_id']
            v.category = body['category']
            v.bitrate = body['bitrate']
            v.save()

            response = {
                "guild_id": int(v.guild_id.id),
                "channel_id": v.channel_id,
                "category": v.category,
                "bitrate": v.bitrate
            }

            return JsonResponse(data=response, status=200)
        else:
            # Return 404 if object not exist
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)