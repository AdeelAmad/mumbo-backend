import base64
import json
import requests
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Guild
import mysql.connector
import sys

sys.path.append('../mumbo')
from counting.models import Count
from leveling.models import levelingsetting, userlevel, rankreward
from voicechannels.models import voicechannelsetting

def init_db():
    return mysql.connector.connect(
        user="",
        password="",
        host="",
        port=10002,
        database="s2_Data"
    )

def get_cursor(conn):
    try:
        conn.ping(reconnect=True, attempts=3, delay=5)
    except:
        # reconnect your cursor as you did in __init__ or wherever
        conn = init_db()
    return conn.cursor(buffered=True)

conn = init_db()

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
                        "waifu": g.waifu,
                        "alert": g.alert
                    }

                    return JsonResponse(data=response, status=200)
                # Return 404 if object not exist
                return HttpResponse(status=404)
            except:
                return HttpResponse(status=400)


        # Post to create guild object if 404 returned from GET method or on server join
        elif request.method == "POST":
            try:
                # If guild object exists
                body = json.loads(request.body)

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
                    guild.voicechannelsetting_set.create()
                    guild.levelingsetting_set.create()

                    return HttpResponse(status=200)
            except:
                return HttpResponse(status=400)


        # PATCH to update data
        elif request.method == "PUT":
            try:
                body = json.loads(request.body)
                if Guild.objects.filter(id=body['id']):
                    g = Guild.objects.get(id=body['id'])
                    g.counting = body['counting']
                    g.voicechannel = body['voicechannel']
                    g.leveling = body['leveling']
                    g.afkmusic = body['afkmusic']
                    g.waifu = body['waifu']
                    g.alert = body['alert']
                    g.save()
                    response = {
                        "id": g.id,
                        "counting": g.counting,
                        "voicechannel": g.voicechannel,
                        "leveling": g.leveling,
                        "afkmusic": g.afkmusic,
                        "waifu": g.waifu,
                        "alert": g.alert
                    }
                    return JsonResponse(data=response, status=200)
                else:
                    # Return 404 if object not exist
                    return HttpResponse(status=404)
            except:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://agradehost.com')

def migrate(request):
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
                body = json.loads(request.body)
                guildobject = Guild.objects.get(id=body['id'])
                if guildobject.migrated == False:
                # Check if guild object exists for guild
                    if len(str(body['id'])) == 18:
                        countobject = Count.objects.get(guild_id=body['id'])
                        levelingobject = levelingsetting.objects.get(guild_id=body['id'])
                        voiceobject = voicechannelsetting.objects.get(guild_id=body['id'])

                        results = {}
                        users = {}

                        cur = get_cursor(conn)
                        cur.execute("SELECT guildID, prefix, createchannel, category, countchannel, currentcount, lastcounter, setlevelupchannel FROM GuildSettings WHERE guildId={}".format(body['id']))
                        for g in cur:
                            results['1'] = {
                                "createchannel": g[2],
                                "createcategory": g[3],
                                "countingchannel": g[4],
                                "currentcount": g[5],
                                "lastcounter": g[6],
                                "levelupchannel": g[7]
                            }


                        cur.execute("SELECT guildID, fun, core, counting, leveling, usertrackingpriot, alertsent FROM GuildModules WHERE guildId={}".format(body['id']))
                        for g in cur:
                            results['2'] = {
                                "fun": g[1],
                                "core": g[2],
                                "counting": g[3],
                                "leveling": g[4]
                            }

                        cur.execute("SELECT guildID, guild, user, xp, xpboost, lastsenttime FROM UserData WHERE guild={}".format(body['id']))
                        for u in cur:
                            levelingobject.userlevel_set.create(user_id=u[2], xp=u[3])

                        if results:
                            guild = {
                                "id": str(body['id']),
                                "counting": results['2']['counting'] == 1,
                                "voicechannel": results['2']['core'] == 1,
                                "leveling": results['2']['leveling'] == 1,
                                "afkmusic": results['2']['fun'] == 1,
                            }

                            lvlsetting = {
                                "id": str(body['id']),
                                "levelupchannel": results['1']['levelupchannel']
                            }

                            vcsettings = {
                                "id": str(body['id']),
                                "channel_id": results['1']['createchannel'],
                                "category": results['1']['createcategory'],
                            }

                            scount = {
                                "id": str(body['id']),
                                "channel": results['1']['countingchannel'],
                                "last_count": results['1']['currentcount'],
                                "last_counter": results['1']['lastcounter']
                            }

                            guildobject.counting = guild['counting']
                            guildobject.voicechannel = guild['voicechannel']
                            guildobject.leveling = guild['leveling']
                            guildobject.afkmusic = guild['afkmusic']
                            guildobject.migrated = True
                            guildobject.save()

                            countobject.channel = scount['channel']
                            countobject.last_count = scount['last_count']
                            countobject.last_counter = scount['last_counter']
                            countobject.save()

                            levelingobject.levelupchannel = lvlsetting['levelupchannel']
                            levelingobject.save()

                            voiceobject.channel_id = vcsettings['channel_id']
                            voiceobject.category = vcsettings['category']
                            voiceobject.save()

                            finaldata = {
                                "guild": guild,
                                "leveling": lvlsetting,
                                "voicechannels": vcsettings,
                                "counting": scount
                            }

                            return JsonResponse(data=finaldata, status=200)
                        else:
                            guildobject.migrated = True
                            guildobject.save()
                            return HttpResponse(status=406)
                # Return 404 if object not exist
                return HttpResponse(status=404)
            except Exception as e:
                print(e)
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=405)
    else:
        return redirect('https://agradehost.com')
