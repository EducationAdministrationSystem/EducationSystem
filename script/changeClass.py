# coding:UTF-8

from users.models import StudentProfile,SmallClass
from const.models import SchoolYear

student_list = {}
rfile = open("../b.txt")
for line in rfile:
    s=line.strip().split('\t')
    # student_list.append(int(s[1]))
    student_list[int(s[1])] = s[0]
rfile.close()
count = len(student_list)
print count

smallclass=SmallClass.objects.filter(class_name="数模2班")[0]

for stu_num, stu_name in student_list.iteritems():
    print stu_num, stu_name
    try:
        student = StudentProfile.objects.get(baseinfo_studentid=str(stu_num))
    except:
        print "no this student"
        continue
    if student.small_class.class_name == u"创新创业工程与实践":
        print student.small_class.class_name
        student.small_class = smallclass
    if student.innovation_grade == 2014:
        print student.innovation_grade
        student.innovation_grade = 2016
    student.save()
