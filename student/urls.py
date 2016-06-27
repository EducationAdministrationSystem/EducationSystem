
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from student import views as student_views

urlpatterns = patterns('',
    url(
        r'^homepage$',
        student_views.selfinfoViews,
    ),
    
    url(
       r'^modify_password$',
        student_views.modifyPasswordViews
    ),
    url(
       r'^homework_submit$',
        student_views.homeworkSubmitViews
    ),

    url(
       r'^homework_submit/(?P<hsid>.{36})$',
        student_views.homeworkSubmitViews
    ),
    url(
       r'^studentselfinfo/(?P<sid>\w+)$',
        student_views.selfinfoViews
    ),
    url(
        r'^schedule$',
        student_views.scheduleViews
    ),
    url(
        r'^selectcourse$',
        student_views.selectCourseViews
    ),
    url(
        r'^score$',
        student_views.scoreViews
    ),
    url(
        r'^classSelect$',
        student_views.classSelectViews
       ),
    url(
        r'^deletecourse$',
        student_views.deleteCourseViews
    ),
    url(
        r'^classchange$',
        student_views.classChangeViews
    ),
    url(
        r'^comment$',
        student_views.commentViews
    ),
   url(
       r'^courseplan$',
       student_views.courseplanViews
   
    ),
    url(
       r'^teacherselfinfo/(?P<tid>\w+)$',
        student_views.teacherSelfinfoViews
    ),
)

urlpatterns += staticfiles_urlpatterns()
