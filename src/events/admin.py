from django.contrib import admin

from .models import Event, Location

admin.site.register(Location)
admin.site.register(Event)
