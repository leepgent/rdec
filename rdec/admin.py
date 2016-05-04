from django.contrib import admin

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
