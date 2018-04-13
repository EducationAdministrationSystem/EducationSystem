#!/usr/bin/env python
# coding=utf-8

from common.models import PracticeClassPractice
from users.models import SmallClass

student_list = []
small_class=SmallClass.objects.all()[1]
print small_class
student_list = PracticeClassPractice.objects.filter(student__small_class__brother_class = small_class)
print student_list.count()
