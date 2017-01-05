from django.contrib import admin
from django.conf import settings

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_filter = ['location', 'date']
    ordering = ['date']


@admin.register(models.EventRole)
class EventRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LeagueMemberEventAttending)
class LeagueMemberEventAttendingAdmin(admin.ModelAdmin):
    list_filter = ['user__name']


@admin.register(models.VisitorEventAttending)
class VisitorEventAttendingAdmin(admin.ModelAdmin):
    list_filter = ['name']


admin.site.site_header = f'RDEC Administration :: {settings.LEAGUE_NAME}'
admin.site.site_title = f'RDEC Administration :: {settings.LEAGUE_NAME}'
admin.site.index_title = 'Add or remove events, roles, visiting attendees or tweak the user account list!'
