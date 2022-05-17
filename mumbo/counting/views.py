import base64
import json
from django.shortcuts import redirect

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Count
import sys
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
            try:
                # Check if Count object exists for guild
                if Count.objects.filter(guild_id=json.loads(request.body)['id']):
                    # Serialize into json
                    response = json.loads(serializers.serialize("json", Count.objects.filter(guild_id=json.loads(request.body)['id'])))[0]['fields']
                    return JsonResponse(data=response, status=200)
                # Return 404 if object not exist
                return HttpResponse(status=404)
            except:
                return HttpResponse(status=400)


        # Post to create count object if 404 returned from GET method or on server join
        elif request.method == "POST":
            # If count object exists
            try:
                if Count.objects.filter(guild_id=json.loads(request.body)['id']):
                    # would create conflict to have two count objects
                    return HttpResponse(status=409)
                else:
                    # Get the Guild object
                    guild = Guild.objects.get(pk=json.loads(request.body)['id'])
                    # Create count object w/ guild foreign key
                    guild.count_set.create()
                    return HttpResponse(status=200)
            except:
                return HttpResponse(status=400)

        # PATCH to update data
        elif request.method == "PUT":
            body = json.loads(request.body)
            if Count.objects.filter(guild_id=body['id']):
                try:
                    c = Count.objects.get(guild_id=body['id'])
                    c.channel = body['channel']
                    c.last_count = body['last_count']
                    c.last_counter = body['last_counter']
                    c.save()
                    response = {
                        "id": c.guild_id.id,
                        "channel": c.channel,
                        "last_count": c.last_count,
                        "last_counter": c.last_counter
                    }
                    return JsonResponse(data=response, status=200)
                except:
                    return HttpResponse(status=400)
            else:
                # Return 404 if object not exist
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://mumbobot.xyz')