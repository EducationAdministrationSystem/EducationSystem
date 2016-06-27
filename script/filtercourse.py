# coding: UTF-8

from common.models import SelectCourse

student_list=[]
for line in open("../course.txt"):
    student_list.append(int(line))
    

selectcourse=SelectCourse.objects.filter(course__course_id__course_plan_id=1160165040)
print selectcourse.count()
count=0
for item in selectcourse:
    student_id=item.student.baseinfo_studentid
    #print student_id 
    student_id=int(student_id)
    if student_id in student_list:
        pass
    else:
        item.delete()
        count=count+1

print count



