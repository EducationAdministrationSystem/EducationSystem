# coding: UTF-8
from const import *
from const.models import ClassTime,WeekTime

for c in CLASSTIME_CHOICES:
    print c[0]
    classTime = ClassTime()
    classTime.category = c[0]
    classTime.save()

print "end"

for c in WEEKTIME_CHOICES:
    week = WeekTime()
    week.category =c[0]
    week.save()

print "end"
