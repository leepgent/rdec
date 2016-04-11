from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from rdec.models import EventRole


@login_required
def personal_dashboard(request):
    now = timezone.now()
    user = request.user
    # For every league I'm a member of:
    # for every future event:
    # show my attendance info

    league2events = dict()

    for league_affiliation in user.leagueaffiliation_set.all():
        league = league_affiliation.league
        league2events[league] = league.event_set.filter(date__gt=now)

    context = {
        'roles': EventRole.objects.all(),
        'league2events': league2events
    }

    return render(request, 'rdec/personaldashboard.html', context)

