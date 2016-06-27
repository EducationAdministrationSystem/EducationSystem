#!/usr/bin/env python
# coding=utf-8
from django.contrib import admin
from student.models import *

RegisterClass = (
    ChangeClassApply,

)

for temp in RegisterClass:
    admin.site.register(temp)
