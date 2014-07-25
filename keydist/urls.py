from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = patterns('',
    url(r'^accounts/', include('accounts.urls', namespace = 'accounts')),
    url(r'^keys/', include('keys.urls', namespace = 'keys')),
    url(r'^$', include('home.urls', namespace = 'home')),
)