
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from practice import views as practice_views

urlpatterns = patterns('',
    url(
        r'^homepage$',
        practice_views.selfinfoViews,
    ),
    url(
        r'^course$',
        practice_views.courseViews,
    ),
    url(
       r'^modify_password$',
        practice_views.modifyPasswordViews
    ),
    url(
       r'^selfinfo$',
        practice_views.selfinfoViews
    ),
    url(
        r'^check_comment$',
        practice_views.check_commentViews,
    ),
    url(
        r'^studentmanage$',
        practice_views.studentmanageViews,
    ),
    url(
        r'^studentmanage/search$',
        practice_views.studentmanageSearchViews,
    ),
    url(
        r'^studentselfinfo/(?P<sid>\w+)$',
        practice_views.studentselfinfoViews
    ),
    url(
        r'^entry$',
        practice_views.recruitEntryViews,
    ),
    url( 
        r'^courseplan$',
        practice_views.coursePlanViews
    ),
    url(
        r'^teachermanage$',
        practice_views.teachermanage
    ),
)

urlpatterns += staticfiles_urlpatterns()
