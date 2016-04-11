from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
urlpatterns = [
    url(r'^$', views.personal_dashboard, name='home'),
    url(r'^signup/', views.SignupView.as_view(), name='signup'),
    url(r'^login/', views.LoginView.as_view(), name='hello'),
    url(r'^logout/', views.logoutview, name='bye'),
    url(r'^change_attending/', login_required(views.ChangeAttendingView.as_view()), name='change_attending')
]
