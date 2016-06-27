# coding: UTF-8

from common.models import PracticeClassPractice,TeacherProfile

teacher=TeacherProfile.objects.filter(userid__username="10620")[0]
print teacher
practicelist=PracticeClassPractice.objects.filter(student__small_class__brother_class=teacher.small_class.brother_class,class_select_5_4=True)

for item in practicelist:
    print item.student
    item.class_select_5_4=False
    item.class_select_5_6=True
    item.save()



