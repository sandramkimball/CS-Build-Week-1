# admin allows you to auto build a site to crud records, useful during testing?
from django.contrib import admin
from .models import Room, Player

admin.site.register(Room)
admin.site.register(Player)
