import xlrd
import xlwt
from common.models import CoursePlan,Course
from const.models import *
from users.models import TeacherProfile
from backend.logging import loginfo
ROW_DICT={
    "course_id"       :1,
    "teacher"         :5,
    "class_week"      :8,
    "class_time"      :9,
    "class_place"     :10,
    "course_to_class" :-1,
    "practice_periods":4,
    "theory_periods"  :3,
    "class_capacity"  :7,
    "start_year"      :11,
}


workbook = xlrd.open_workbook("1.xlsx")
table = workbook.sheet_by_index(0)
errors= []
course_list = []
for i in range(1,table.nrows):
    row = table.row_values(i)
    course = Course()
    try:
        course.course_id = CoursePlan.objects.get(course_plan_id = row[ROW_DICT["course_id"]])
        if course.course_id.course_name != row[ROW_DICT["course_id"]+1]:
            raise ValueError('')
    except:
        errors.append([i,ROW_DICT["course_id"]])
        errors.append([i,ROW_DICT["course_id"]+1])
        print "error"
    try:
        course.practice_periods = int(row[ROW_DICT["practice_periods"]])
    except:
        errors.append([i,row[ROW_DICT["practice_periods"]]])
    try:
        course.theory_periods = int(row[ROW_DICT["theory_periods"]])
    except:
        errors.append([i,row[ROW_DICT["theory_periods"]]])
    try:
        course.teacher = TeacherProfile.objects.get(teacher_id = int(row[ROW_DICT["teacher"]]))
        if course.teacher.teacher_name != row[ROW_DICT["teacher"]+1]:
            raise ValueError('')
    except:
        errors.append([i,ROW_DICT["teacher"]])
        errors.append([i,ROW_DICT["teacher"]+1])
        print "error"
    try:
        course.class_capacity = int(row[ROW_DICT["class_capacity"]])
    except:
        errors.append([i,ROW_DICT["class_capacity"]])
    try:
        course.class_place = ClassRoom.objects.get(room_name=row[ROW_DICT["class_place"]])
    except:
        errors.append([i,ROW_DICT["class_place"]])
    try:
        course.start_year = SchoolYear.objects.get(school_year=row[ROW_DICT["start_year"]])
    except:
        errors.append([i,ROW_DICT["start_year"]])
    try:
        weeks = WeekTime.objects.filter(category__in = course.get_class_week_list(row[ROW_DICT["class_week"]]))
    except:
        errors.append([i,ROW_DICT["class_week"]])
    for i in errors:
        print i[0],i[1]
    course_list.append([course,weeks])

if len(errors) == 0:
    for item,weeks in course_list:
        item.save()
        [item.class_week.add(i) for i in weeks]

print "end"
