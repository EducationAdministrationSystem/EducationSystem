#!/usr/bin/env python
# coding=utf-8

from django.contrib import admin
from const.models import *

RegisterClass = (
    ClassTime,
    WeekTime,
    AdminSetting,
    SchoolYear,
    UserIdentity,
    ClassRoom
)


for item in RegisterClass:
    admin.site.register(item)
