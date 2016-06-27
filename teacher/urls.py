
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from teacher import views as teacher_views

urlpatterns = patterns('',
    url(
        r'^homepage$',
        teacher_views.selfinfoViews,
    ),
    url(
       r'^modify_password$',
        teacher_views.modifyPasswordViews
    ),
    url(
       r'^studentselfinfo/(?P<sid>\w+)$',
        teacher_views.studentselfinfoViews
    ),
    url(
        r'^scoreManagement$',
        teacher_views.ratioManagementViews,
    ),
    url(
        r'^homeworkManagement$',
        teacher_views.homeworkManagementViews,
    ),
    url(
        r'^scoreManagement/ratio',
        teacher_views.ratioManagementViews,
    ),
    url(
        r'^scoreManagement/score',
        teacher_views.scoreManagementViews,
    ),

    url(
        r'^classRemain$',
        teacher_views.classRemainViews,
    ),
    url(
        r'^classChange/(?P<teachertype>\w+)$',
        teacher_views.classChangeViews,
    ),
    url(
        r'^classInfo$',
        teacher_views.classListQueryViews,
    ),
    url(
        r'^classInfo/classList',
        teacher_views.classListQueryViews,
    ),
    url(
        r'^assessment$',
        teacher_views.assessmentViews,
    ),
    url(
        r'^classInfo/scoreList',
        teacher_views.scoreListQueryViews,
    ),
    url(
        r'^classInfo/scoreSearch',
        teacher_views.studentScoreSearchViews,
    ),
    url(
        r'^classInfo/studentList',
        teacher_views.studentListQueryViews,
    ),
    url(
        r'^studentmanage$',
        teacher_views.studentmanageViews,
    ),
    url(
        r'^studentmanage/search$',
        teacher_views.studentmanageSearchViews,
    ),
    url(
        r'^schedule$',
        teacher_views.teacherScheduleViews,
    ),
    url(
        r'practiceclass/(?P<grade>\d)$',
        teacher_views.practiceclassViews,
    )
)

urlpatterns += staticfiles_urlpatterns()
