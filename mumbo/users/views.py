import base64
import json
import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import discorduser


@csrf_exempt
def index(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
    except:
        return redirect('https://agradehost.com')

    if username == "bot" and password == "%a_938xZeT_VcY8J7uN7GGHnw4auuvVQ":
        # GET to retrieve data
        if request.method == "GET":
            try:
                if discorduser.objects.filter(user_id=json.loads(request.body)['user_id']):
                    u = discorduser.objects.get(user_id=json.loads(request.body)['user_id'])
                    response = {
                        "user_id": u.user_id,
                        "month": u.month,
                        "day": u.day
                    }
                    return JsonResponse(data=response, status=200)
                else:

                    responsedict = {}

                    response = discorduser.objects.all().order_by("month", "day")

                    for r in response:
                        d = datetime.datetime.now()
                        month = int(d.strftime("%m").lstrip('0'))
                        date = int(d.strftime("%d").lstrip('0'))


                        if r.month > month-1:
                            if r.month == month:
                                if date < r.day:
                                    responsedict[r.user_id] = r.month, r.day
                            else:
                                responsedict[r.user_id] = r.month, r.day

                    return JsonResponse(responsedict, status=200)


                # INPUT: USER ID
                # OUTPUT: MONTH + DAY
                #return the month and day for user
            except Exception as e:
                print(e)
                return HttpResponse(status=400)

        # Post to create count object if 404 returned from GET method or on server join
        elif request.method == "POST":
            # If count object exists
            try:
                if discorduser.objects.filter(user_id=json.loads(request.body)['user_id']):
                    # would create conflict to have two count objects
                    return HttpResponse(status=409)
                else:
                    discorduser(user_id=json.loads(request.body)['user_id']).save()
                    return HttpResponse(status=200)
            except Exception as e:
                return HttpResponse(status=400)

        # PATCH to update data
        elif request.method == "PUT":
            body = json.loads(request.body)
            if discorduser.objects.filter(user_id=body['user_id']):
                try:
                    u = discorduser.objects.get(user_id=body['user_id'])
                    u.month = body['month']
                    u.day = body['day']
                    u.save()
                    # GET USER OBJECT AND SWAP OUT THE VALUES

                    response = {
                        "user_id": u.user_id,
                        "month": u.month,
                        "day": u.day
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
        return redirect('https://agradehost.com')
