# coding:UTF-8

from common.models import SelectCourse,Course,Score
from users.models import StudentProfile,SmallClass
from const.models import SchoolYear
from django.contrib.auth.models import User

student_list = {}
try:
    rfile = open("../df.txt")
    for line in rfile:
        s=line.strip().split('\t')
        # student_list.append(int(s[1]))
        student_list[int(s[1])] = s[0]
    rfile.close()
except Exception, e:
    print e
    pass

count = len(student_list)
schoolyear = SchoolYear.objects.filter(school_year="2016-2017")
schoolyear=schoolyear[0]
print schoolyear
course = Course.objects.filter(course_id__course_plan_id="1160165090")
print course
course=course[0]
course.int_nelepeo = count
course.save()

for stu_num in student_list:
    try:
        student = StudentProfile.objects.get(baseinfo_studentid=str(stu_num))
    except:
        try:
            user=User.objects.create_user(username=stu_num,password=stu_num)
            user.save()
        except:
            user=User.objects.get(username=stu_num)
        smallclass=SmallClass.objects.filter(class_name="创新创业工程与实践")
        student=StudentProfile(userid=user,small_class=smallclass[0])
        student.baseinfo_name=student_list[stu_num]
        student.baseinfo_studentid=str(stu_num)
        student.save()
    if SelectCourse.objects.filter(student=student,course=course).count()==0:
        selectcourse_obj = SelectCourse()
        selectcourse_obj.student = student
        selectcourse_obj.course = course
        selectcourse_obj.save()
    else:
        selectcourse_obj=SelectCourse.objects.filter(student=student,course=course)[0]
    if Score.objects.filter(select_obj=selectcourse_obj).count()==0:
        score = Score()
        score.select_obj = selectcourse_obj
        score.save()
