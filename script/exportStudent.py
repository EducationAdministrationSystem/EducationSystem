# coding:UTF-8
from users.models import StudentProfile
from django.db.models import Q


# student_list = StudentProfile.objects.filter(innovation_grade = 2014).order_by("baseinfo_studentid")
student_list = StudentProfile.objects.filter(Q(innovation_grade = 2014) | Q(innovation_grade = 2015) | Q(innovation_grade = 2016)).order_by("innovation_grade", "baseinfo_studentid")
print len(student_list)



outfile = open("../../student.csv",'w')
import csv
writer = csv.writer(outfile)
writer.writerow(["姓名", "学号", "创院班级", "原班级", "年级"])
for stu in student_list:
    # print stu.baseinfo_studentid
    # print stu.baseinfo_name
    # print stu.small_class
    # print stu.collegeinfo_class
    name = stu.baseinfo_name.encode("UTF-8").ljust(14)
    stuid = stu.baseinfo_studentid.encode("UTF-8").ljust(10)
    if stu.small_class:
        smallclass = stu.small_class.class_name.encode("UTF-8").ljust(40)
    else:
        smallclass = ""
    if stu.collegeinfo_class:
        originclass = stu.collegeinfo_class.encode("UTF-8").ljust(40)
    else:
        originclass = ""
    innovation_grade = str(stu.innovation_grade).encode("UTF-8").ljust(10)
    print name, stuid, smallclass, originclass, innovation_grade
    writer.writerow([name, stuid, smallclass, originclass, innovation_grade])
    # info = name+"\t"+stuid+"\t"+sex+"\t"+tel+"\t"+apartment+"\t"+college+"\t"+first+"\t"+second+"\t"+adjust+"\r\n"
    # outfile.write(info)
outfile.close()
