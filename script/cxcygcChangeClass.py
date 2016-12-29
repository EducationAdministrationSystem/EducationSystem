# coding:UTF-8

from users.models import StudentProfile,SmallClass
from const.models import SchoolYear
from student.models import ChangeClassApply
from django.contrib.auth.models import User

# student_list = []
# rfile = open("../s.txt")
# for line in rfile:
#     # s=line.strip().split('\t')
#     student_list.append(int(line))
#     # student_list[int(s[1])] = s[0]
# rfile.close()
# count = len(student_list)
# print count


smallclass=SmallClass.objects.filter(class_name="创新创业工程与实践")[0]
student_list = StudentProfile.objects.filter(small_class = smallclass,baseinfo_studentid__contains = "2016",innovation_grade = 2014)
print len(student_list)

for student in student_list:
    print student.small_class.class_name
    print student.baseinfo_studentid
    print student.innovation_grade
    print student.baseinfo_name
    userset = User.objects.filter(username = student.baseinfo_studentid)
    changeClassApply = ChangeClassApply.objects.filter(student = student)
    if changeClassApply:
        changeClassApply[0].delete()
    student.delete()
    userset[0].delete()

    # try:
    #     if userset:
    #         print "now delete"
    #         print student
    #         userset[0].delete()
    #     else:
    #         print "has deleted"
    #         print student
    # except Exception, e:
    #     print e
    #     print "*****"
    #     print student
    #     continue
