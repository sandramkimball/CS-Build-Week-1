from django.db import models

# @csrf_exempt
# @api_view(["POST"])
# def get_rooms(request):
#     dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
#     reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
#     room = request.user.room
#     room_id = room.id
#     room_uuid = room.uuid
#     data = json.loads(request.body)
#     direction = data['direction']
#     room = player.room()
#     nextRoomID = None
#     if direction == "n":
#         nextRoomID = room.n_to
#     elif direction == "s":
#         nextRoomID = room.s_to
#     elif direction == "e":
#         nextRoomID = room.e_to
#     elif direction == "w":
#         nextRoomID = room.w_to
#     if nextRoomID is not None and nextRoomID > 0:
#         nextRoom = Room.objects.get(id=nextRoomID)
#         player.currentRoom=nextRoomID
#         player.save()
#         players = nextRoom.playerNames(player_id)
#         currentPlayerUUIDs = room.playerUUIDs(player_id)
#         nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
#         return JsonResponse({'room':room.name, 'title':nextRoom.title, 'description':nextRoom.description, 'players':players, 'error_msg':""}, safe=True)
#     else:
#         players = room.playerNames(player_id)
#         return JsonResponse({'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


