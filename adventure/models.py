from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid


class Chamber(models.Model):
    title = models.CharField(max_length=50, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    u_to = models.IntegerField(default=0)
    d_to = models.IntegerField(default=0)

    def connectChambers(self, destinationChamber, direction):
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
