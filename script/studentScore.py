# coding:UTF-8

from common.models import SelectCourse,Course,Score
from users.models import StudentProfile,SmallClass
from const.models import SchoolYear
from django.contrib.auth.models import User
import csv

student_list = StudentProfile.objects.filter(innovation_grade = 2014)
print "总人数: %d" % len(student_list)

outfile = open("../2014.csv",'wb')
writer = csv.writer(outfile)
writer.writerow(["姓名", "学号", "入学年份", "课程名称", "成绩"])
# student_list = student_list[:10]

for stu in student_list:
    name = stu.baseinfo_name.encode("UTF-8").ljust(14)
    stuid = stu.baseinfo_studentid.encode("UTF-8").ljust(10)
    grade = stu.innovation_grade
    write_list = [name, stuid, grade]
    # print '%s, %s, %d' % (name, stuid, grade)
    select_course = SelectCourse.objects.filter(student = stu)
    for sle_cou in select_course:
        try:
            course_name = sle_cou.course.course_id.course_name.encode("UTF-8").ljust(30)
            total_score = Score.objects.get(select_obj = sle_cou).total
            # print '%s, %d' % (course_name, total_score)
            write_list.append(course_name)
            write_list.append(total_score)
        except:
            pass
    writer.writerow(write_list)
outfile.close()
