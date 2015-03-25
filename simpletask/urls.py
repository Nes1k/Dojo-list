from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',
    url(r'^', include('core.urls')),
    (r'^accounts/', include('allauth.urls')),
)
