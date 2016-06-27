# coding: UTF-8
from django.shortcuts import render
from django.contrib.auth.models import User
from backend.logging import loginfo
from django.http import HttpResponseRedirect,HttpResponse
from users.models import StudentProfile, User, TeacherProfile, SmallClass
from common.views import common_selfinfoViews, common_modifyPasswordViews
from const.models import AdminSetting
from student.forms import StudentInfoForm, SelectSmallClassForm,ClassChangeForm, CommentForm
from student.models import ChangeClassApply
from common.models import Course, PracticeClassPractice,SelectCourse, Score, Homework, HomeworkSubmit, CoursePlan, SmallClassPractice
from django.views.decorators import csrf
from const import *
import datetime
from backend.decorators import *
from django.views.decorators import csrf
from common.utility import selectCourseContext,DeleteCourseContext
from common.utility import getStudentGrade
from teacher.forms import HomeworkForm
from django.db.models import Q


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def modifyPasswordViews(request):


    context = {
        'modify_password_info':common_modifyPasswordViews(request),

    }
    return render(request,"student/modify_password.html",context)


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def selfinfoViews(request,sid = None):
    student = StudentProfile.objects.get(userid = request.user)
    context = common_selfinfoViews(request,student.baseinfo_studentid)
    return render(request,"student/self_info.html",context)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def scheduleViews(request):
    student=StudentProfile.objects.get(userid=request.user)
    schedule=[["" for i in range(7)] for j in range(6)]
    adminSetting=AdminSetting.objects.all()[0]
    school_year=adminSetting.school_year
    school_term=adminSetting.school_term
    select_course=student.selectcourse_set.filter(Q(course__start_year=school_year)&(Q(course__course_id__course_term=school_term)|Q(course__course_id__course_term=-1)))
    print select_course
    for item in select_course:
        class_time=item.course.class_time.all()
        for t in class_time:
            schedule[t.category%10-1][t.category/10-1]=item.course.course_id.course_name+"<br/>"+u"地点："+item.course.class_place.room_name+"<br/>"+u"上课周："+item.course.get_class_week_display()
    context={"schedule":schedule}
    return render(request,"student/schedule_table.html",context)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def selectCourseViews(request):
    student=StudentProfile.objects.get(userid=request.user)
    context=selectCourseContext(request,student)
    context["role"] = "student"
    return render(request,"student/select_course.html",context)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def deleteCourseViews(request):
    student=StudentProfile.objects.get(userid=request.user)
    context=DeleteCourseContext(student)
    return render(request,"student/delete_course.html",context)
@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def scoreViews(request):

    student = StudentProfile.objects.get(userid = request.user)
    selects = SelectCourse.objects.filter(student = student)
    for select in selects:
        select.score = Score.objects.get(select_obj = select)
    context = {
            "selects": selects,
    }
    return render(request, "student/score_table.html", context)
@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def classSelectViews(request):
    student = StudentProfile.objects.get(userid = request.user)
    smallClass = student.small_class.brother_class
    print smallClass
    smallClassPractice = SmallClassPractice.objects.filter(small_class = smallClass, class_grade = getStudentGrade(student))
    if smallClassPractice.count()>0:
        smallClassPractice=smallClassPractice[0]
    else:
        return render(request, "student/class_select_table.html", {"status":1})
    selectSmallClass, fg = PracticeClassPractice.objects.get_or_create(student = student)
    context = {"status":0}
    if request.method == "POST":
        selectSmallClassForm = SelectSmallClassForm(request.POST, instance = selectSmallClass)
        if selectSmallClassForm.is_valid():
            obj = selectSmallClassForm.save(commit = False)
            fieldName = 'class_select_%d_%d'
            cnt = 0
            for i in range(1, 8):
                for j in range(1, 7):
                    if selectSmallClassForm.cleaned_data[fieldName % (i, j)]:
                        if cnt >= 2:
                            setattr(obj, fieldName % (i, j), False)
                            print getattr(obj, fieldName % (i, j), False)
                        else: cnt += 1
            obj.save()
    selectSmallClassForm = SelectSmallClassForm(instance = selectSmallClass)

    for i in range(1, 8):
        for j in range(1, 7):
            remainFieldName = "class_remain_%d_%d" % (i, j)
            selectFieldName = "class_select_%d_%d" % (i, j)
            classRemain = getattr(smallClassPractice, remainFieldName)
            kwargs = {}
            kwargs["small_class__brother_class"] = smallClass
            kwargs["practiceclasspractice__class_select_%d_%d" % (i, j)] = True
            kwargs["innovation_grade"]=student.innovation_grade
            students = StudentProfile.objects.filter(**kwargs)
            context["class_remain_%d_%d" % (i, j)] = classRemain - students.count()
    selectSmallClassForm.update(context = context)
    context["selectSmallClassForm"] = selectSmallClassForm
    return render(request, "student/class_select_table.html", context)


from django.core.files.storage import default_storage
@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def homeworkSubmitViews(request):
    user =  User.objects.get(id = request.user.id)

    stu = StudentProfile.objects.get(userid = user)
    course_all = SelectCourse.objects.filter(student = stu)



    course_counter = 1
    file_upload_error = 0
    if request.method == "POST":
        if request.FILES.has_key('file'): 
            course_counter =  int(request.POST['course_counter'])
            if request.FILES['file'].size > 10 * 1024 * 1024:
                file_upload_error = 2 # file more 1MB
            else:
                hid = request.POST['hid']
                hw = Homework.objects.get(id = hid)
                submit = HomeworkSubmit.objects.filter(homework = hw, student = stu)
                file_upload_error = 1 # upload success
                if submit:
                    submit = submit[0]
                    default_storage.delete(submit.homework_file.path)
                    submit.homework_file = request.FILES['file']
                    submit.submit_time = datetime.datetime.now()
                    submit.save()
                else:
                    submit = HomeworkSubmit()
                    submit.student = stu
                    submit.homework = hw
                    submit.homework_file = request.FILES['file']
                    submit.submit_time = datetime.datetime.now()
                    submit.save()

    course_list = []
    for c in course_all:
        homework_all = list(Homework.objects.filter(course = c.course))
        homework_all.sort(cmp=lambda x, y: -cmp(x.homework_rank, y.homework_rank))
        homework_list = []
        for h in homework_all:
            dic_h = vars(h)
            cnt = HomeworkSubmit.objects.filter(homework = h, student = stu)
            if cnt:
                dic_h['submitted'] = cnt[0]
            else:
                dic_h['submitted'] = None
            homework_list.append(dic_h)

        dic_c = vars(c.course)
        dic_c['name'] = c.course
        dic_c['homework_list'] = homework_list
        course_list.append(dic_c)

    data = {
        'course_list':course_list,
        'course_counter':course_counter,
        'file_upload_error':file_upload_error,
        'now_datetime': datetime.datetime.now(),
        'homework_form':HomeworkForm()
    }


    return render(request, "student/homework_submit.html", data)



@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def classChangeViews(request):
    student = StudentProfile.objects.get(userid = request.user)
    originclass = student.small_class
    changeapply = ChangeClassApply.objects.filter(student = student)
    adminSetting=AdminSetting.objects.all()[0]
    switch=adminSetting.class_change_switch
    message = ""
    if request.method == "POST":
        if switch==False:
            message=u"非转班阶段不许允转班申请！"
            classchangeform = ClassChangeForm(request.POST)
        else:
            if changeapply:
                classchangeform = ClassChangeForm(request.POST,instance = changeapply[0])
                if changeapply[0].originOK == AGREE_CHOICE_UNDFINED:
                    if classchangeform.is_valid():
                        classchangeform.save(student,originclass)
                        message = u"保存成功"
                    else:
                        message = u"输入信息不对"
                        print classchangeform.errors
                else:
                    message = u"已经开始审核不允许再修改" 
            else:
                classchangeform = ClassChangeForm(request.POST)
                if classchangeform.is_valid():
                    classchangeform.save(student,originclass)
                    message = u"保存成功"
                else:
                    message = u"输入信息不对"
                    print classchangeform.errors
    else:
        classchangeform = ClassChangeForm()
    changeapply = ChangeClassApply.objects.filter(student = student)
    context = {
            'classchangeform':classchangeform,
            'message':message,
            'changeapply':changeapply,
            'AGREE_CHOICE_UNDFINED':AGREE_CHOICE_UNDFINED
        }
    return render(request,"student/changeclass.html",context)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def commentViews(request):
    stu = StudentProfile.objects.get(userid = request.user)
    course_all = SelectCourse.objects.filter(student = stu)
    #if comment_form.is_valid():
    #comment_content=trip_str(comment_form.cleaned_data["comment"])

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            comment = data['comment']
            course_id = data['courseid']
            course = SelectCourse.objects.get(id = course_id)
            course.evalution = comment
            course.save()
        else:
            pass
    comment_form = CommentForm()
    context = {
        'course_list':course_all, 
        'form':comment_form
    }
    return render(request, "student/comment.html", context)

def courseplanViews(request):
    student=StudentProfile.objects.get(userid=request.user)
    practice=student.small_class.practice_class
    courseplanlist=practice.courseplan_set.all()
    context={
        "practice":practice,
        "courseplanlist":courseplanlist
    }
    return render(request,"student/courseplan.html",context)

@login_required
@authority_required(STUDENT_USER)
def teacherSelfinfoViews(request,tid):
    teacher = TeacherProfile.objects.get(teacher_id = tid)
    context = {
        'teacher':teacher,
    }
    return render(request,"student/teacher_info.html",context)
