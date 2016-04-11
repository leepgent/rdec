from django.db import models
from django.conf import settings


class League(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LeagueAffiliation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    league = models.ForeignKey('League')
    is_event_admin = models.BooleanField(default=False)

    def __str__(self):
        admin_token = ' (A)' if self.is_event_admin else ''
        return '{}/{}{}'.format(self.user, self.league, admin_token)


class Event(models.Model):
    league = models.ForeignKey('League')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()


class EventRole(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class EventAttending(models.Model):
    class Meta:
        abstract = True

    event = models.ForeignKey('Event')
    role = models.ForeignKey('EventRole')


class LeagueMemberEventAttending(EventAttending):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)


class VisitorEventAttending(EventAttending):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)
