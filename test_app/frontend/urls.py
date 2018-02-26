from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/(?P<id>\d+)/$', views.user_profile, name='user_profile'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^home/$', views.home, name='home'),
]

