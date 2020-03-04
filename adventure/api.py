from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from .mars import *
from rest_framework.decorators import api_view
import json
from rest_framework import serializers, viewsets

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

class ChamberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chamber
        fields = ('id_num', 'name', 'description', 'n_to', 's_to', 'e_to', 'w_to')

class ChamberViewSet(viewsets.ModelViewSet):
    serializer_class = ChamberSerializer
    queryset = Chamber.objects.all()

@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    chamber = player.chamber()
    players = chamber.playerNames(player_id)
    return JsonResponse({'uuid': uuid, 'name':player.user.username, 'chamber':chamber.name, 'description':chamber.description, 'players':players}, safe=True)

@csrf_exempt
@api_view(['GET'])
def chambers(request):
    user = request.user
    player = request.player
    allChambers = [{'id':chamber.id_num, 'name':chamber.name, 'description':chamber.description, 'n_to': chamber.n_to, 's_to': chamber.s_to, 'e_to': chamber.e_to, 'w_to': chamber.w_to, 'players': chamber.playerNames(player.id)} for chamber in Chamber.objects.all()]
    return JsonResonse(allChambers, safe=False)

@csrf_exempt
@api_view(['GET'])
def mars(request):
    
    Mars = {'width':mars.width, 'mars':mars.height, 'grid':mars.grid, 'description':'The Red Planet'}
    return JsonResonse(Mars, safe=False)

# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    chamber = player.chamber()
    nextChamberID = None
    if direction == "n":
        nextChamberID = chamber.n_to
    elif direction == "s":
        nextChamberID = chamber.s_to
    elif direction == "e":
        nextChamberID = chamber.e_to
    elif direction == "w":
        nextChamberID = chamber.w_to
    if nextChamberID is not None and nextChamberID > 0:
        nextChamber = Chamber.objects.get(id=nextChamberID)
        player.currentChamber=nextChamberID
        player.save()
        players = nextChamber.playerNames(player_id)
        currentPlayerUUIDs = chamber.playerUUIDs(player_id)
        nextPlayerUUIDs = nextChamber.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'name':player.user.username, 'name':nextChamber.title, 'description':nextChamber.description, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = chamber.playerNames(player_id)
        return JsonResponse({'name':player.user.username, 'chamber':chamber.name, 'description':chamber.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)

@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)
