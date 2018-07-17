#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-07-23 18:07
# Last modified: 2017-07-23 18:52
# Filename: ajax.py
# Description:
# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template.loader import render_to_string
from django.db.models import Q
from common.models import Homework, HomeworkSubmit, Course, SelectCourse, Score, SmallClassPractice
from teacher.forms import HomeworkForm,TeacherAddForm,SmallClassForm
from dajaxice.utils import deserialize_form
from forms import RatioSetForm
from users.models import *
from backend.logging import *
from common.utility import getHomeworkScore,getYearbyGrade

@dajaxice_register
def getStatistics(request, course_id):
    score_set = Score.objects.filter(select_obj__course__id = course_id)
    if score_set.count():
        tot = score_set.count()
        var_1 = 1.0 * score_set.filter(total__gte = 90).count() / tot
        var_2 = 1.0 * score_set.filter(total__gte = 60).count() / tot - var_1
        var_3 = 1 - var_1 - var_2
    else:
        var_1, var_2, var_3 = 0, 0, 0
    return "优秀：%.2f，良好：%.2f，不及格：%.2f" % (var_1, var_2, var_3)
@dajaxice_register
def submitCourse(request, course_id):
    course = Course.objects.get(id = course_id)
    course.is_finished = True
    course.save()
    return simplejson.dumps({"course_id": course_id, })

@dajaxice_register
def getCourseMembers(request, course_id):
    message = "ok"
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return simplejson.dumps({"message": u"未查询到该门课程的相关成绩",
                                 "status": "2"})
    rates = [course.attendance_rate, course.homework_rate, course.final_rate]
    if not any(filter(lambda x: x, rates)):
        return simplejson.dumps({"message": u"请先设置该门课程的系数比例",
                                 "status": '1'})
    selects = SelectCourse.objects.filter(course__id=course_id).order_by('student__baseinfo_studentid')
    for select in selects:
        tmp_score = Score.objects.filter(select_obj=select)
        if tmp_score:
            select.score = tmp_score[0]
        else:
            # score = Score()
            # score.select_obj = select
            # score.save()
            # select.score = score
            continue
        # select.score = Score.objects.get(select_obj = select)        
        select.homework = getHomeworkScore(select.student, select.course)
    sub_html = render_to_string("teacher/widgets/sub_score_checkin.html", {"selects": selects, "course": course, })
    total_html = render_to_string("teacher/widgets/total_score_checkin.html", {"selects": selects, "course": course, })

    return simplejson.dumps({"message": message, "sub_html": sub_html,
                             "status": '0', "total_html": total_html})

@dajaxice_register
def getEditform(request):
    teacher = TeacherProfile.objects.get(userid = request.user)
    form = TeacherAddForm(initial={
        'baseinfo_teacherid':teacher.teacher_id,        
        'baseinfo_name':teacher.teacher_name,
        'small_class':teacher.small_class.id,    
        'teacher_email':teacher.teacher_email,
        'teacher_telephone':teacher.teacher_telephone,
        'office_address':teacher.office_address,
        'office_phone':teacher.office_phone,            
        })
    teacherEdit_html = render_to_string("widgets/teacher_edit.html",{'form':form})
    context={
        'teacherEdit_html':teacherEdit_html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def EditSelfInfo(request,form):
    editform = TeacherAddForm(deserialize_form(form))
    teacher = TeacherProfile.objects.get(userid = request.user)
    if editform.is_valid():
        data = editform.cleaned_data
        # teacher.teacher_id=data['baseinfo_teacherid']
        teacher.teacher_name=data['baseinfo_name']
        smallclass = SmallClass.objects.get(id =  data['small_class'])
        teacher.small_class=smallclass
        teacher.teacher_email=data['teacher_email']
        teacher.teacher_telephone=data['teacher_telephone']
        teacher.office_phone=data['office_phone']
        teacher.office_address=data['office_address']
        teacher.save()
        message="修改成功"
    else:
        message="请正确输入信息"
    selfinfo_html = render_to_string('widgets/teacher_info.html',{'teacher':teacher})
    context={
        'message':message,
        'selfinfo_html':selfinfo_html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def fillForm(request, course_id):
    message = ""
    course = Course.objects.get(id = course_id)
    form = RatioSetForm(instance = course)
    html = render_to_string("teacher/widgets/ratio_set_form.html", {"form": form})
    return simplejson.dumps({"message": message, "html": html,})

@dajaxice_register
def saveRatio(request, course_id, var_1, var_2, var_3):
    course = Course.objects.get(id = course_id)
    message = ""
    try:
        var_1, var_2, var_3 = map(int, (var_1, var_2, var_3))
    except:
        message = "error"
        return simplejson.dumps({"message": message, })

    if sum((var_1, var_2, var_3)) != 100:
        message = "unfit"
        return simplejson.dumps({"message": message, })
    else:
        course.attendance_rate = var_1
        course.homework_rate = var_2
        course.final_rate = var_3
        course.save()
        message = "ok"
        return simplejson.dumps({"message": message, })

@dajaxice_register
def scoreCheckIn(request, select_id, var_1, var_2, var_3):
    message = ""
    select = SelectCourse.objects.get(id = select_id)
    try:
        var_1, var_2, var_3 = map(int, (var_1, var_2, var_3))
    except:
        message = "error"
        return simplejson.dumps({"message": message, })
    try:
        if not (0 <= var_1 <= 100 and 0 <= var_2 <= 100 and 0 <= var_3 <= 100):
            raise

        score = Score.objects.get(select_obj = select)
        score.attendance = var_1
        score.homework = var_2
        score.final = var_3
        score.total = select.course.calculate_score(var_1, var_2, var_3)
        score.save()
    except:
        message = "overflow"
        return simplejson.dumps({"message": message, })
    
    message = "ok"
    return simplejson.dumps({"message": message, "total": score.total,})

def refreshHomeworkTable(course):

    homework_list = list(Homework.objects.filter(course = course))
    homework_list.sort(cmp=lambda x, y: -cmp(x.homework_rank, y.homework_rank))

    context = {
        'course':{
            'homework_list': homework_list,

        }
    }    
    return render_to_string('teacher/widgets/homework_table.html', context)

@dajaxice_register
def saveHomework(request, form, cid, hid):


    form = HomeworkForm(deserialize_form(form))

    context = {
        'status': 0,
        'error_list':"",
        'homework_table':"",

    }
    error_list = ""
    if form.is_valid():        
        if hid:
            h = Homework.objects.get(id = hid)
        else:
            h = Homework()
            h.course = Course.objects.get(id = cid)
            h.homework_rank = len(Homework.objects.filter(course = h.course)) + 1

        h.name = form.cleaned_data['name']
        h.required = form.cleaned_data['required']
        h.deadline = form.cleaned_data['deadline']
        h.is_final = form.cleaned_data['is_final']
        h.save()
        context['homework_table'] = refreshHomeworkTable(h.course)
    else :
        for key in form.errors:
            error_list += (str(key) + ",")
        context['status'] = 1
        context['error_list'] = error_list
    return simplejson.dumps(context)

@dajaxice_register
def getHomeworkSubmitTable(request, hid):

    homework_submit_list = HomeworkSubmit.objects.filter(homework_id = hid)

    context = {
        'homework_submit_list': homework_submit_list,

    }
    homework_submit_table = render_to_string('teacher/widgets/homework_submit_table.html', context)

    context = {
        'homework_submit_table':homework_submit_table,
    }

    
    return simplejson.dumps(context)
@dajaxice_register
def saveScore(request, form, hsid):
    
    form = deserialize_form(form)

    data = {
        'status': 0,
        'score':None,

    }

    score_str = form['score']
    if len(score_str) == 0:
        data['status'] = 1
    elif len(score_str) > 9:
        data['status'] = 2
    elif not score_str.isdigit():
        data['status'] = 3
    else :

        hs = HomeworkSubmit.objects.get(id = hsid)
        hs.score = int(score_str)
        hs.save()
        data['status'] = 0
        data['score'] = hs.score
    return simplejson.dumps(data) 

@dajaxice_register
def getComment(request,courseid):
    course = Course.objects.get(id=courseid)
    evalutionlist = [obj.evalution for obj in SelectCourse.objects.filter(course=course)]
    # evalutionlist = SelectCourse.objects.filter(course=course)
    context ={
        'evalutionlist':evalutionlist,
    }
    form_html = render_to_string("widgets/evalution.html",context)
    return simplejson.dumps({"form_html":form_html})

@dajaxice_register
def getSmallClass(request, grade):
    teacher = TeacherProfile.objects.get(userid = request.user)
    smallClass = teacher.small_class.brother_class
    smallClassPractice, _ = SmallClassPractice.objects.get_or_create(small_class = smallClass, class_grade = grade)
    context = {"grade":grade}
    smallClassForm = SmallClassForm(instance = smallClassPractice)
    context["smallClassForm"] = smallClassForm
    year=getYearbyGrade(grade)

    for i in range(1, 8):
        for j in range(1, 7):
            remainFieldName = "class_remain_%d_%d" % (i, j)
            selectFieldName = "class_select_%d_%d" % (i, j)
            classRemain = getattr(smallClassPractice, remainFieldName)
            kwargs = {}
            kwargs["small_class__brother_class"] = smallClass
            kwargs["practiceclasspractice__class_select_%d_%d" % (i, j)] = True
            kwargs["innovation_grade"]=year
            students = StudentProfile.objects.filter(**kwargs)
            context["class_selected_%d_%d" % (i, j)] = students.count()
    return render_to_string("teacher/widgets/classRemainTable.html",
                                context)

@dajaxice_register
def updateSmallClass(request, form, grade):
    teacher = TeacherProfile.objects.get(userid = request.user)
    smallClass = teacher.small_class.brother_class
    smallClassPractice = SmallClassPractice.objects.get(small_class = smallClass, class_grade = grade)
    loginfo(smallClass)
    smallClassForm = SmallClassForm(deserialize_form(form), instance = smallClassPractice)
    if smallClassForm.is_valid():
        print "small class update form is valid"
        smallClassForm.save()
    else: print "small class update form is not valid!"
    context = {"grade":grade}
    context["smallClassForm"] = smallClassForm
    year=getYearbyGrade(grade)
    for i in range(1, 8):
        for j in range(1, 7):
            remainFieldName = "class_remain_%d_%d" % (i, j)
            selectFieldName = "class_select_%d_%d" % (i, j)
            classRemain = getattr(smallClassPractice, remainFieldName)
            kwargs = {}
            kwargs["small_class__brother_class"] = smallClass
            kwargs["practiceclasspractice__class_select_%d_%d" % (i, j)] = True
            kwargs["innovation_grade"]=year
            students = StudentProfile.objects.filter(**kwargs)
            context["class_selected_%d_%d" % (i, j)] = students.count()
    return render_to_string("teacher/widgets/classRemainTable.html",
                                context)
