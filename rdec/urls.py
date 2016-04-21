from django.conf.urls import url
from django.contrib.auth.decorators import login_required
import django.contrib.auth.views

from . import views
urlpatterns = [
    url(r'^$', views.personal_dashboard, name='home'),
    url(r'^favicon.ico$', views.favicon, name='favicon'),
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', views.LoginView.as_view(), name='hello'),
    url(r'^logout/', views.logoutview, name='bye'),
    url(r'^profile/', login_required(views.ProfileView.as_view()), name='profile'),
    url(r'^change_attending/', login_required(views.ChangeAttendingView.as_view()), name='change_attending'),
    url(r'^events/$', views.eventlist, name='eventlist'),
    url(r'^events/(?P<event_slug>[\w-]+)-(?P<event_id>\w+)/', views.eventdetails, name='eventdetails'),

    url(r'^user/password/reset/$', django.contrib.auth.views.password_reset,
        {
            'post_reset_redirect':
                '/user/password/reset/done/',
            'template_name': 'reg/password_reset_form.html',
            'email_template_name': 'reg/password_reset_email.html',
            'subject_template_name': 'reg/password_reset_subject.txt'

        },
        name="password_reset"),
    url(r'^user/password/reset/done/$', django.contrib.auth.views.password_reset_done,
        {
            'template_name': 'reg/password_reset_done.html'
        }),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        django.contrib.auth.views.password_reset_confirm,
        {
            'post_reset_redirect': '/user/password/done/',
            'template_name': 'reg/password_reset_confirm.html'
        }, name='password_reset_confirm'),
    url(r'^user/password/done/$', django.contrib.auth.views.password_reset_complete,
        {
            'template_name': 'reg/password_reset_complete.html'
        })
]
