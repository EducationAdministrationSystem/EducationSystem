# coding:UTF-8

#  统计２０１６自然年各个实践班的授课情况
# 课程门数　教学学时　实验人时数　学生规模


from users.models import SmallClass, PracticeProfile
from common.models import Course, CoursePlan
from const.models import SchoolYear
from django.db.models import Q

start_year1 = SchoolYear.objects.get(school_year = "2015-2016")
start_year2 = SchoolYear.objects.get(school_year = "2016-2017")

courses = Course.objects.all()
courses = courses.filter(course_id__course_practice__nick_name = 'rxjqr')
courses = courses.filter((Q(start_year = 4) & Q(course_id__course_term = 2)) | (Q(start_year = 5) & Q(course_id__course_term = 1)))
print len(courses)

ret = []
theory_periods = 0
practice = 0
count = 0

for course in courses:
    print course
    print course.start_year
    theory_periods += course.theory_periods
    practice += course.practice_periods * course.int_nelepeo
    count += course.int_nelepeo

print "*********************"
print "课程门次数："
print len(courses)
print "教学学时"
print theory_periods
print "实验人时数"
print practice
print "学生规模"
print count
