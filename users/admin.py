#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from users.models import *

RegisterClass = (
    SmallClass,
    TeacherProfile,
    PracticeProfile,
    AdminStaffProfile,
    PresidentProfile,
)

class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ['baseinfo_name','baseinfo_studentid']

class ApplyInfoAdmin(admin.ModelAdmin):
    search_fields = ['student_id', 'student_name']

admin.site.register(StudentProfile,StudentProfileAdmin)
admin.site.register(ApplyInfo, ApplyInfoAdmin)
for temp in RegisterClass:
    admin.site.register(temp)
