import base64
import json
from django.shortcuts import redirect

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import levelingsetting, userlevel, rankreward, xpeditevent
import sys
from sentry_sdk import capture_message

sys.path.append('../mumbo')

from management.models import Guild

@csrf_exempt
def index(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
    except:
        return redirect('https://mumbobot.xyz')
    if username == "bot" and password == "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ":
        # GET to retrieve data
        if request.method == "GET":
            # Check if Count object exists for guild
            if levelingsetting.objects.filter(guild_id=json.loads(request.body)['id']):
                # Serialize into json
                response = json.loads(serializers.serialize("json", levelingsetting.objects.filter(guild_id=json.loads(request.body)['id'])))[0]['fields']
                return JsonResponse(data=response, status=200)
            # Return 404 if object not exist
            return HttpResponse(status=404)


        # Post to create count object if 404 returned from GET method or on server join
        elif request.method == "POST":
            # If count object exists
            if levelingsetting.objects.filter(guild_id=json.loads(request.body)['id']):
                # would create conflict to have two count objects
                return HttpResponse(status=409)
            else:
                # Get the Guild object
                guild = Guild.objects.get(pk=json.loads(request.body)['id'])
                # Create count object w/ guild foreign key
                guild.levelingsetting_set.create()
                return HttpResponse(status=200)


        # PATCH to update data
        elif request.method == "PUT":
            body = json.loads(request.body)

            if levelingsetting.objects.filter(guild_id=body['id']):
                l = levelingsetting.objects.get(guild_id=body['id'])
                l.global_boost = body['global_boost']
                l.levelupchannel = body['levelupchannel']
                l.save()
                response = {
                    "id": l.guild_id.id,
                    "global_boost": l.global_boost,
                    "levelupchannel": l.levelupchannel
                }
                return JsonResponse(data=response, status=200)
            else:
                # Return 404 if object not exist
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://mumbobot.xyz')

@csrf_exempt
def pain(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
    except:
        return redirect('https://mumbobot.xyz')
    if username == "bot" and password == "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ":


        # GET to retrieve data
        if request.method == "GET":
            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['guild_id'])

            # Check if guild object exists for guild
            if userlevel.objects.filter(user_id=body['id'], guild=setting):

                u = userlevel.objects.get(user_id=body['id'], guild=setting)

                response = {
                    "guild": u.guild.guild_id.id,
                    "user_id": u.user_id,
                    "xp": u.xp,
                    "last_message": u.last_message
                }

                return JsonResponse(data=response, status=200)
            # Return 404 if object not exist
            return HttpResponse(status=404)

        # Post to create guild object if 404 returned from GET method or on server join
        elif request.method == "POST":
            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['guild_id'])

            # If guild object exists
            if userlevel.objects.filter(user_id=body['id'], guild=setting):
                # would create conflict to have two guild objects
                return HttpResponse(status=409)
            else:
                # Get the levelingsettings object
                setting = levelingsetting.objects.get(guild_id=body['guild_id'])

                # Create userlevel object w/ levelingsetting foreign key
                setting.userlevel_set.create(user_id=body['id'])

                return HttpResponse(status=200)

        # PATCH to update data
        elif request.method == "PUT":

            # logger for edits

            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['guild_id'])

            if userlevel.objects.filter(user_id=body['id'], guild=setting):
                u = userlevel.objects.get(user_id=body['id'], guild=setting)
                old_xp = u.xp
                u.xp = body['xp']
                u.save()

                response = {
                    "guild": u.guild.guild_id.id,
                    "user_id": u.user_id,
                    "xp": u.xp,
                    "last_message": u.last_message
                }

                capture_message("User: {} Old XP: {} Awarded XP: {} New XP: {}".format(u.user_id, old_xp, body['xp']-old_xp, u.xp))

                return JsonResponse(data=response, status=200)
            else:
                # Return 404 if object not exist
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://mumbobot.xyz')

def leaderboard(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
    except:
        return redirect('https://mumbobot.xyz')
    if username == "bot" and password == "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ":
        # GET to retrieve data
        if request.method == "GET":
            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['id'])

            responsedict = {}

            response = userlevel.objects.filter(guild=setting).order_by("-xp")[:10]

            for r in response:
                responsedict[r.user_id] = r.xp

            return JsonResponse(data=responsedict, status=200)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://mumbobot.xyz')

@csrf_exempt
def pain2(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
    except:
        return redirect('https://mumbobot.xyz')
    if username == "bot" and password == "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ":


        # GET to retrieve data
        if request.method == "GET":
            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['guild_id'])

            # Check if guild object exists for guild
            if rankreward.objects.filter(guild=setting):

                r = rankreward.objects.filter(guild=setting)

                response = {}
                counter = 1

                for rank in r:
                    response[counter] = {
                    "guild": rank.guild.guild_id.id,
                    "role_id": rank.role_id,
                    "level": rank.level,
                    }
                    counter += 1
                return JsonResponse(data=response, status=200)
            # Return 404 if object not exist
            return HttpResponse(status=404)

        # Post to create guild object if 404 returned from GET method or on server join
        elif request.method == "POST":
            body = json.loads(request.body)
            setting = levelingsetting.objects.get(guild_id=body['guild_id'])

            # If guild object exists
            if rankreward.objects.filter(role_id=body['role_id'], guild=setting):
                # would create conflict to have two rank rewards objects for same role
                return HttpResponse(status=409)
            else:
                # Create userlevel object w/ levelingsetting foreign key
                setting.rankreward_set.create(role_id=body['role_id'], level=body['level'])

                return HttpResponse(status=200)

        elif request.method == "DELETE":
            body = json.loads(request.body)
            # If guild object exists
            if rankreward.objects.filter(role_id=body['role_id']):
                rr = rankreward.objects.get(role_id=body['role_id'])
                rr.delete()
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=404)

    else:
        return redirect('https://mumbobot.xyz')
