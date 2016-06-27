
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from president import views as president_views

urlpatterns = patterns('',
    url(
        r'^homepage$',
        president_views.courseViews,
    ),
    url(
       r'^practice$',
        president_views.practiceViews,
    )
)
