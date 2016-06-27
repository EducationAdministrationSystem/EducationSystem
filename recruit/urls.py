
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from recruit import views as recruit_views

urlpatterns = patterns('',
    url(
        r'^$',
        recruit_views.homeViews,
    ),
    url(
        r'^registration$',
        recruit_views.registrationViews,
    ),
    url(
        r'^response$', 
        recruit_views.responseViews,
    ),
    url(
        r'^mobile',
        recruit_views.homeMobileViews,
    ),
    url(
        r'^responseMobile',
        recruit_views.responseMobileViews,
    ),
)

urlpatterns += staticfiles_urlpatterns()



