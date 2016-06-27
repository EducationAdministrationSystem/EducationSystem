#encoding=utf-8
from common.models import SelectCourse,Course,CoursePlan
from django.db.models import Q
from const.models import AdminSetting
from users.models import *

teacher = TeacherProfile.objects.get(teacher_name = "李胜铭")
admin_setting = AdminSetting.objects.all()[0]
school_year = admin_setting.school_year
school_term = admin_setting.school_term
course = Course.objects.filter(Q(teacher = teacher)
                              &Q(start_year__school_year = school_year)
                              &Q(course_id__course_term = school_term))

# student_set = set()

# students = SelectCourse.objects.filter(course = course[0])
# for item in students:
#     selectCourse = SelectCourse()
#     selectCourse.student = item.student
#     selectCourse.course = course[3]
#     student_set.add(item.student)
#     selectCourse.save()

# students = SelectCourse.objects.filter(course = course[1])
# for item in students:
#     if item.student in student_set:continue
#     selectCourse = SelectCourse()
#     selectCourse.student = item.student
#     selectCourse.course = course[3]
#     selectCourse.save()
#     student_set.add(item.student)

# c = course[3]
# c.class_capacity = 80
# c.int_nelepeo = 76
# c.save()

print course
course[1].class_capacity = 76
print course[1].class_capacity
course[1].save()




