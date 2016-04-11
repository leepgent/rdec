from django.contrib import admin

from . import models

admin.site.register(models.Event)
admin.site.register(models.EventRole)
admin.site.register(models.LeagueMemberEventAttending)
admin.site.register(models.VisitorEventAttending)
