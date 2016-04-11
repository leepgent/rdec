from django.db import models
from django.conf import settings


class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return '{} at {} on {}'.format(self.name, self.location, self.date)


class EventRole(models.Model):
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.role


class EventAttending(models.Model):
    class Meta:
        abstract = True

    event = models.ForeignKey('Event')
    role = models.ForeignKey('EventRole')

    def __str__(self):
        return 'attending {} as {}'.format(self.event, self.role)


class LeagueMemberEventAttending(EventAttending):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{} {}'.format(self.user, super(LeagueMemberEventAttending, self).__str__())


class VisitorEventAttending(EventAttending):
    name = models.CharField(max_length=100)
    contact_details = models.CharField(max_length=100)

    def __str__(self):
        return 'Visitor {} {}'.format(self.name, super(VisitorEventAttending, self).__str__())
