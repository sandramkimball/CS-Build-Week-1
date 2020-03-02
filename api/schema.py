from django.conf import from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import Player

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player
        interfaces = (graphene.relay.Node, ) #tuple

class Query(graphene.ObjectType):
    players = graphene.List(PlayerType)

    def resolve_players(self, info):
        return Player.objects.all()

schema = graphene.Schema(query=Query)