from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random
import json
import uuid



class Chamber(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0, null=True, blank=True)
    s_to = models.IntegerField(default=0, null=True, blank=True)
    e_to = models.IntegerField(default=0, null=True, blank=True)
    w_to = models.IntegerField(default=0, null=True, blank=True)
    u_to = models.IntegerField(default=0, null=True, blank=True)
    d_to = models.IntegerField(default=0, null=True, blank=True)
    # x = models.IntegerField(default=0, null=True, blank=True)
    # y = models.IntegerField(default=0, null=True, blank=True)
    
    def connect_chambers(self, destinationChamber, direction):
        destinationChamberID = destinationChamber.id
        try:
            destinationChamber = Chamber.objects.get(id=destinationChamberID)
        except Chamber.DoesNotExist:
            print("That chamber does not exist")
            
        else:
            if direction == "n":
                self.n_to = destinationChamberID
            elif direction == "s":
                self.s_to = destinationChamberID
            elif direction == "e":
                self.e_to = destinationChamberID
            elif direction == "w":
                self.w_to = destinationChamberID
            elif direction == "u":
                self.u_to = destinationChamberID
            elif direction == "d":
                self.d_to = destinationChamberID
            else:
                print("Invalid direction")
                return
            self.save()

    def convert_to_dict(self):
        """Returns a dictionary representation of this class including metadata such as the module and class names"""
        #  Populate the dictionary with object meta data
        obj_dict = {"__class__": self.__class__.__name__, "__module__": self.__module__}
        #  Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
        if self.n_to is not None:
            obj_dict['n_to'] = self.n_to
        if self.s_to is not None:
            obj_dict['s_to'] = self.s_to
        if self.e_to is not None:
            obj_dict['e_to'] = self.e_to
        if self.w_to is not None:
            obj_dict['w_to'] = self.w_to
        if self.u_to is not None:
            obj_dict['u_to'] = self.u_to
        if self.d_to is not None:
            obj_dict['d_to'] = self.d_to
        return obj_dict

    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]

    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentChamber=self.id) if p.id != int(currentPlayerID)]


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentChamber = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def initialize(self):
        if self.currentChamber == 0:
            self.currentChamber = Chamber.objects.first().id
            self.save()

    def chamber(self):
        try:
            return Chamber.objects.get(id=self.currentChamber)
        except Chamber.DoesNotExist:
            self.initialize()
            return self.chamber()




@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()

class Alien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.IntegerField(default=0, 0) #lat long
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    health = models.IntegerField(blank=True) # 150/200
    attack = models.IntegerField(blank=True) # randomize.floor(1, 50)
    
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()

    def room(self):
        try:
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

