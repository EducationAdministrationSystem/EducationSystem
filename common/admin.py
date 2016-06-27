#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from common.models import *

RegisterClass = (
    CoursePlan,
    Course,
    SelectCourse,
    Score,
    PracticeClassPractice,
    Homework,
    HomeworkSubmit,
    SmallClassPractice,
)

for item in RegisterClass:
    admin.site.register(item)
