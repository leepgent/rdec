from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import View
from django.conf import settings

from rdec.models import EventRole, Event, LeagueMemberEventAttending


class _EventAndAttendance(object):
    def __init__(self, event):
        self.event = event
        self.response = None
        self.is_recent = False
        self.elapsed = 0


@login_required
def personal_dashboard(request):
    now = timezone.now()
    then = now - timedelta(days=1)
    user = request.user

    # for every future event:
    # show my attendance info

    recency_cutoff_secs = float(settings.RECENT_EVENT_CUTOFF_DAYS) * 24 * 60 * 60

    events = Event.objects.filter(date__gt=then).order_by('date')
    event_attendances = list()

    for event in events:
        b = _EventAndAttendance(event)
        elapsed = (now - event.last_modified)
        b.is_recent = elapsed.total_seconds() < recency_cutoff_secs
        b.elapsed = elapsed.total_seconds()
        try:
            b.response = event.leaguemembereventattending_set.get(user=user)
        except LeagueMemberEventAttending.DoesNotExist:
            pass

        event_attendances.append(b)

    context = {
        'roles': EventRole.objects.all(),
        'event_attendances': event_attendances,
        'recency_cutoff': settings.RECENT_EVENT_CUTOFF_DAYS,
        'recency_cutoff_secs': recency_cutoff_secs

    }

    return render(request, 'rdec/personaldashboard.html', context)


class SignupView(View):
    def get(self, request):
        next = request.GET.get('next', None)
        context = {
            'next': next
        }
        return render(request, 'rdec/signup.html', context)

    def post(self, request):
        email = request.POST['email_field']
        name = request.POST['name_field']
        password1 = request.POST['password1_field']
        password2 = request.POST['password2_field']
        next = request.POST['next']

        try:
            validate_email(email)
        except:
            messages.warning(request, 'Your e-mail address was not in the correct format. Sorry!')
            return render(request, 'rdec/signup.html')

        if password1 != password2:
            messages.warning(request, 'Your passwords did not match!')
            return render(request, 'rdec/signup.html')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'This e-mail address is already in use!')
            return render(request, 'rdec/signup.html')

        if User.objects.filter(first_name=name).exists():
            messages.warning(request, 'This name address is already in use!')
            return render(request, 'rdec/signup.html')

        new_user = User.objects.create_user(email, email=email, password=password1)
        new_user.first_name = name
        new_user.save()

        new_user = authenticate(username=email, password=password1)
        login(request, new_user)

        return HttpResponseRedirect(reverse('home'))


class LoginView(View):
    def get(self, request):
        return render(request, 'rdec/signin.html')

    def post(self, request):
        username = request.POST['username_field']
        password = request.POST['password_field']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Account disabled.', content_type='text/plain')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, 'Your username and password did not match. Sorry!')
            return render(request, 'rdec/signin.html')


@login_required
def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


class ChangeAttendingView(View):
    def post(self, request):
        event_id = request.POST['event_id']
        new_status = request.POST['new_status']
        user = request.user

        event = Event.objects.get(pk=event_id)
        if new_status == 'null':
            LeagueMemberEventAttending.objects.filter(user=user, event=event).delete()
            return HttpResponse()

        status = EventRole.objects.get(pk=new_status)

        LeagueMemberEventAttending.objects.filter(user=user, event=event).delete()  # TODO: fix this bug properly!

        thing = LeagueMemberEventAttending(user=user, role=status, event=event)
        thing.save()
        return HttpResponse()
        # I need user (from request), event id from payload, new attending status (or null for removal)


class _EventSummary(object):
    def __init__(self, event):
        self.event = event
        self.role_map = dict()


@login_required
def eventlist(request):
    now = timezone.now()

    then = now - timedelta(days=1)

    events = Event.objects.filter(date__gt=then).order_by('date')
    roles = EventRole.objects.all()

    eventlist = list()

    for event in events:
        es = _EventSummary(event)

        for role in roles:
            es.role_map[role] = dict()
            es.role_map[role]['members'] = list()
            es.role_map[role]['visitors'] = list()
        for member_attending in event.leaguemembereventattending_set.all():
            es.role_map[member_attending.role]['members'].append(member_attending)
        for visitor_attending in event.visitoreventattending_set.all():
            es.role_map[visitor_attending.role]['visitors'].append(visitor_attending)

        eventlist.append(es)

    context = {
        'roles': roles,
        'eventlist': eventlist
    }
    return render(request, 'rdec/eventlist.html', context)


def eventdetails(request, event_slug, event_id):
    event = get_object_or_404(Event, pk=event_id)
    roles = EventRole.objects.all()

    eventmap = dict()

    for role in roles:
        eventmap[role] = dict()
        eventmap[role]['members'] = list()
        eventmap[role]['visitors'] = list()
    for member_attending in event.leaguemembereventattending_set.all():
        eventmap[member_attending.role]['members'].append(member_attending)
    for visitor_attending in event.visitoreventattending_set.all():
        eventmap[visitor_attending.role]['visitors'].append(visitor_attending)

    context = {
        'event': event,
        'roles': roles,
        'eventmap': eventmap
    }
    return render(request, 'rdec/eventdetails.html', context)


class ProfileView(View):
    def get(self, request):
        return render(request, 'rdec/profile.html')

    def post(self, request):
        user = request.user
        changed = False

        if 'change_name' in request.POST:
            new_name = request.POST['change_name']
            if new_name:
                existing = User.objects.filter(first_name=new_name).exists()
                if existing:
                    messages.warning(request, 'The name you supplied has already been used!')
                else:
                    user.first_name = new_name
                    changed = True
        if 'change_mail_1' in request.POST and 'change_mail_2' in request.POST:
            m1 = request.POST['change_mail_1']
            m2 = request.POST['change_mail_2']
            if m1 and m2:
                if m1 != m2:
                    messages.warning(request, 'The email addresses provided did not match!')
                else:
                    existing = User.objects.filter(email=m1).exists()
                    if existing:
                        messages.warning(request, 'The email address you supplied has already been used!')
                    else:
                        user.email = m1
                        user.username = m1
                        changed = True

        if 'change_password_1' in request.POST and 'change_password_2' in request.POST:
            p1 = request.POST['change_password_1']
            p2 = request.POST['change_password_2']
            if p1 and p2:
                if p1 != p2:
                    messages.warning(request, 'The passwords provided did not match!')
                else:
                    user.set_password(p1)
                    changed = True

        if changed:
            user.save()
            messages.info(request, 'Profile Saved!')

        return render(request, 'rdec/profile.html')

