import json
import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import voicechannelsetting, channel
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
                "category": v.category,
                "bitrate": v.bitrate
            }

            return JsonResponse(data=response, status=200)
        # Return 404 if object not exist
        return HttpResponse(status=404)


    # Post to create guild object if 404 returned from GET method or on server join
    elif request.method == "POST":
        body = json.loads(request.body)
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

@csrf_exempt
def pain(request):
    # GET to retrieve data
    if request.method == "GET":
        body = json.loads(request.body)

        # Check if guild object exists for guild
        if channel.objects.filter(channel_id=body['id']):

            v = channel.objects.get(channel_id=body['id'])

            response = {
                "guild": v.guild.guild_id.id,
                "channel_id": v.channel_id,
                "owner": v.owner
            }

            return JsonResponse(data=response, status=200)
        # Return 404 if object not exist
        return HttpResponse(status=404)

    # Post to create guild object if 404 returned from GET method or on server join
    elif request.method == "POST":
        body = json.loads(request.body)
        # If guild object exists
        if channel.objects.filter(channel_id=body['channel_id']):
            # would create conflict to have two guild objects
            return HttpResponse(status=409)
        else:
            # Get the Guild object
            guild = voicechannelsetting.objects.get(guild_id=body['guild_id'])

            # Create voicechannelsetting object w/ guild foreign key
            guild.channel_set.create(channel_id=body['channel_id'], owner=body['owner'])

            return HttpResponse(status=200)

    elif request.method == "DELETE":
        body = json.loads(request.body)
        # If guild object exists
        if channel.objects.filter(channel_id=body['id']):
            chan = channel.objects.get(channel_id=body['id'])
            chan.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
        # PATCH to update data

    elif request.method == "PUT":
        body = json.loads(request.body)
        if channel.objects.filter(channel_id=body['channel_id']):
            c = channel.objects.get(channel_id=body['channel_id'])
            c.owner = body['owner']
            c.save()

            response = {
                "id": int(c.guild.guild_id.id),
                "channel_id": c.channel_id,
                "owner": c.owner
            }

            return JsonResponse(data=response, status=200)
        else:
            # Return 404 if object not exist
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=405)