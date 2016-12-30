#coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from adminStaff import views as adminStaff_views

urlpatterns = patterns('',
    url(
        r'^$',
        adminStaff_views.studentmanageViews
    ),

    url(
        r'^modify_password/student$',
        adminStaff_views.modifyStudentPasswordViews
    ),


    url(
       r'^modify_password$',
        adminStaff_views.modifyPasswordViews
    ),
    url(
       r'^course$',
        adminStaff_views.courseViews
    ),
    url(
       r'^courseExport$',
        adminStaff_views.courseExportViews
    ),
    url(
        r'^studentmanage$',
        adminStaff_views.studentmanageViews
    ),
    url(
        r'^studentmanage/search$',
        adminStaff_views.studentmanage_searchViews
    ),
    url(
       r'^studentselfinfo/(?P<sid>\w+)$',
        adminStaff_views.selfinfoViews
    ),
    url(
        r'^studentmanage/classchange$',
        adminStaff_views.studentmanage_classchangeViews
    ),
    url(
        r'^studentmanage/studentchangeclass$',
        adminStaff_views.studentmanage_studentchangeclassViews
    ),
    url(
        r'^managementsetting$',
        adminStaff_views.managementSettingViews

    ),
    url(
        r'^classRemain$',
        adminStaff_views.classRemainViews
    ),
    url(
        r'^classInfo$',
        adminStaff_views.classListQueryViews,
    ),
    url(
        r'^classInfo/classList',
        adminStaff_views.classListQueryViews,
    ),
    url(
        r'^classInfo/scoreList',
        adminStaff_views.scoreListQueryViews,
    ),
    url(
        r'^classInfo/scoreSearch',
        adminStaff_views.studentScoreSearchViews,
    ),
    url(
        r'^classInfo/studentList',
        adminStaff_views.studentListQueryViews,
    ),
    url(
        r'^admin_comment$',
        adminStaff_views.admin_commentViews
    ),
    url(
        r'^mycourseplan$',
        adminStaff_views.coursePlanViews
    ),
    url(
        r'^selectcourse$',
        adminStaff_views.courseSelectViews
    ),
    url(
        r'^selectcourse/deletecourse$',
        adminStaff_views.courseDeleteViews
    ),
    url(
        r'^selectcourse/coursestatistical$',
        adminStaff_views.courseStatisticalViews
    ),
    url(
        r'^classroom$',
        adminStaff_views.classRoomViews
    ),
    url(
        r'^classroom_add$',
        adminStaff_views.classRoomAddViews
    ),
    url(
        r'^importCourseData',
        adminStaff_views.importCourseData
    )
)
#教师管理url
urlpatterns += patterns('',
    url(
        r'^teachermanage$',
        adminStaff_views.teachermanageViews
    ),
    url(
        r'^teachermanage/search$',
        adminStaff_views.teachermanage_searchViews
    ),

)

#班级管理URL
urlpatterns += patterns("",
    url(
        r'^classmanage$',
        adminStaff_views.classmanageViews
    ),
    url(
        r'^small_class$',
        adminStaff_views.small_classViews
    ),
)

urlpatterns += staticfiles_urlpatterns()
