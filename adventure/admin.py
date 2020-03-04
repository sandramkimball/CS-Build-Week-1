# admin allows you to auto build a site to crud records, useful during testing?
from django.contrib import admin
from .models import Room, Player
from .mars import Chamber, Mars

admin.site.register(Room)
admin.site.register(Mars)
admin.site.register(Chamber)
admin.site.register(Player)
