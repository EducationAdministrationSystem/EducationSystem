#encoding=utf-8
from common.models import PracticeClassPractice
from users.models import SmallClass

student_list = []
small_class=SmallClass.objects.all()[1]
print small_class
student_list = PracticeClassPractice.objects.filter(student__small_class__brother_class = small_class)
print student_list.count()
for item in student_list:
    #print item.student.baseinfo_name
    if item.class_select_1_3 == True:
        item.class_select_1_3 = False
        item.class_select_5_5 = True
    if item.class_select_1_4 == True:
        item.class_select_1_4 = False
        item.class_select_5_6 = True
    if item.class_select_1_5 == True or item.class_select_2_3 == True:
        item.class_select_1_5 = False
        item.class_select_2_3 = False
        item.class_select_6_3 = True
    if item.class_select_1_6 == True or item.class_select_2_4 == True:
        item.class_select_1_6 = False
        item.class_select_2_4 = False
        item.class_select_6_4 = True
    item.save()

