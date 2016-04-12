from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import View

from rdec.models import EventRole, Event, LeagueMemberEventAttending


@login_required
def personal_dashboard(request):
    now = timezone.now()
    user = request.user
    # for every future event:
    # show my attendance info

    events = Event.objects.filter(date__gt=now).order_by('date')
    event_map = dict()
    for event in events:
        response = event.leaguemembereventattending_set.filter(user=user)
        if response.exists():
            response = response[0]
        else:
            response = None
        event_map[event] = response

    context = {
        'roles': EventRole.objects.all(),
        'events': event_map # Event.objects.filter(date__gt=now).order_by('date')
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
        thing = LeagueMemberEventAttending(user=user, role=status, event=event)
        thing.save()
        return HttpResponse()
        # I need user (from request), event id from payload, new attending status (or null for removal)


@login_required
def eventlist(request):
    now = timezone.now()
    user = request.user

    events = Event.objects.filter(date__gt=now).order_by('date')
    roles = EventRole.objects.all()

    eventmap = dict()
    for event in events:
        eventmap[event] = dict()
        for role in roles:
            eventmap[event][role] = dict()
            eventmap[event][role]['members'] = list()
            eventmap[event][role]['visitors'] = list()
        for member_attending in event.leaguemembereventattending_set.all():
            eventmap[event][member_attending.role]['members'].append(member_attending)
        for visitor_attending in event.visitoreventattending_set.all():
            eventmap[event][visitor_attending.role]['visitors'].append(visitor_attending)

    context = {
        'roles': roles,
        'eventmap': eventmap
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
