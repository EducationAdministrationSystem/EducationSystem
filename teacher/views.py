# coding: UTF-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from common.models import Course, Homework, HomeworkSubmit, SelectCourse
from django.http import HttpResponseRedirect,HttpResponse
from common.models import Course, Homework, HomeworkSubmit,PracticeClassPractice
from teacher.forms import HomeworkForm, GradeForm
from django.contrib.auth.models import User
from users.models import TeacherProfile
from django.http import HttpResponseRedirect,HttpResponse
from teacher.forms import SmallClassForm
from users.models import *
from backend.decorators import *
from common.views import common_selfinfoViews, common_modifyPasswordViews
from django.views.decorators import csrf
from common.models import Course
from common.views import common_classchangeViews,common_studentmanageViews,common_studentsearchViews,common_selfinfoViews
from common.forms import CourseFilterForm, StudentFilterForm
from const.models import AdminSetting
from common.utility import getYearbyGrade
from itertools import chain
import datetime
from django.db.models import Q


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def modifyPasswordViews(request):


    context = {
        'modify_password_info':common_modifyPasswordViews(request),

    }
    return render(request,"teacher/modify_password.html",context)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def studentListQueryViews(request):
    form = StudentFilterForm()
    context = {
            "form": form,
        }
    return render(request, "teacher/student_list_query.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def studentScoreSearchViews(request):
    context = {}
    return render(request, "teacher/student_score_search.html", context)
@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def scoreListQueryViews(request):
    form = CourseFilterForm()
    context = {
            "form": form,
        }
    return render(request, "teacher/score_list_query.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def classListQueryViews(request):
    form = CourseFilterForm()
    context = {
            "form": form,
    }
    return render(request, "teacher/class_list_query.html", context)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def selfinfoViews(request):
    teacher =request.user.teacherprofile_set.all()[0]
    return render(request,"teacher/self_info.html",{'teacher':teacher})

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def ratioManagementViews(request):
    teacher = TeacherProfile.objects.get(userid = request.user)
    admin_setting = AdminSetting.objects.all()[0]
    school_year = admin_setting.school_year
    school_term = admin_setting.school_term
    courses1 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term=-1)))
    if school_term == 2:
        school_term = 1
        courses2 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term=-1)))
    elif school_term == 1:
        school_term = 2
        year = school_year.school_year.split("-")
        year[0] = int(year[0].encode("UTF-8"))-1
        year[1] = int(year[1].encode("UTF-8"))-1
        year[0] = str(year[0])
        year[1] = str(year[1])
        year[0] = unicode(year[0],"utf-8")
        year[1] = unicode(year[1],"utf-8")
        school_year = year[0] + "-" + year[1]
        courses2 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term=-1))) 
    context = {
        "courses1": courses1,
        "courses2": courses2
    }
    return render(request, "teacher/ratio_management.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def scoreManagementViews(request):
    print "######"
    now=datetime.datetime.now()
    teacher = TeacherProfile.objects.get(userid = request.user)
    admin_setting = AdminSetting.objects.all()[0]
    score_enter_start=admin_setting.score_enter_start
    score_enter_end=admin_setting.score_enter_end
    school_year = admin_setting.school_year
    school_term = admin_setting.school_term
    message=""
    if now < score_enter_start or now > score_enter_end:
        message=u"非成绩录入阶段不能录入！"
    context={
        "message":message
    }
    #courses1 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term = -1)))
    courses1 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year))
    
    if school_term == 2:
        school_term = 1
        courses2 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term = -1)))
    elif school_term == 1:
        school_term = 2

        year = school_year.school_year.split("-")
        year[0] = int(year[0].encode("UTF-8"))-1
        year[1] = int(year[1].encode("UTF-8"))-1
        year[0] = str(year[0])
        year[1] = str(year[1])
        year[0] = unicode(year[0],"utf-8")
        year[1] = unicode(year[1],"utf-8")
        school_year = year[0] + "-" + year[1]
        courses2 = Course.objects.filter(Q(teacher = teacher)&Q(start_year__school_year = school_year)&(Q(course_id__course_term = school_term )|Q(course_id__course_term = -1)))
    courses = courses1|courses2
    if message =="":
        context.update({
            "courses": courses,
        })


    return render(request, "teacher/score_management.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def homeworkManagementViews(request):
    print "homework : user::" + str(request.user.id)
    # print Course.objects.all()



    user =  User.objects.get(id = request.user.id)
    tea = TeacherProfile.objects.get(userid = user)
    cnt = AdminSetting.objects.all()[0]
    print "**" * 11
    print cnt.school_term
    print cnt.school_year
    course_all = Course.objects.filter(teacher = tea, \
         start_year = cnt.school_year, \
         course_id__course_term = cnt.school_term\
        )
    # course_all = []

    course_list = []
    for c in course_all:
        homework_list = []
        homework_all = list(Homework.objects.filter(course = c))
        homework_all.sort(cmp=lambda x, y: -cmp(x.homework_rank, y.homework_rank))
        for h in homework_all:
            dic_h = vars(h)
            dic_h["homework_sumbit_list"] = HomeworkSubmit.objects.filter(homework = h)
            homework_list.append(dic_h)
        dic_c = vars(c)
        dic_c['name'] = c
        dic_c['homework_list'] = homework_list
        course_list.append(dic_c)

    context = {
        'course_list':course_list,
        'homework_form':HomeworkForm(),
    }
    return render(request, "teacher/homework_management.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def classRemainViews(request):
    context = {}
    context["gradeChoice"] = GradeForm()
    return render_to_response("teacher/classRemain.html", context, context_instance = RequestContext(request))

    # teacher = TeacherProfile.objects.get(userid = request.user)
    # smallClass = teacher.small_class
    # context = {}
    # if request.method == "POST":
    #     smallClassForm = SmallClassForm(request.POST, instance = smallClass)
    #     if smallClassForm.is_valid(): smallClassForm.save()
    # else:
    #     smallClassForm = SmallClassForm(instance = smallClass)
    # context["smallClassForm"] = smallClassForm
    # return render(request, "teacher/classRemain.html", context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def assessmentViews(request):
    tea = TeacherProfile.objects.get(userid = request.user)
    course_all = Course.objects.filter(teacher = tea)
    context={
        'course_list':course_all, 
    }
    return render(request,"teacher/assessment.html",context)



@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def classChangeViews(request,teachertype = "origin"):
    context = common_classchangeViews(request,teachertype)
    return render(request,"teacher/classchange.html",context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def studentmanageViews(request):
    context = common_studentmanageViews(request)
    return render(request,"teacher/studentmanage/studentmanage_add.html",context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def studentmanageSearchViews(request):
    context = common_studentsearchViews(request)
    return render(request,"teacher/studentmanage/studentmanage_search.html",context)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def studentselfinfoViews(request,sid = None):
    context = common_selfinfoViews(request,sid)
    return render(request,"teacher/studentmanage/studentmanage_selfinfo.html",context)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def teacherScheduleViews(request):
    teacher=TeacherProfile.objects.get(userid=request.user)
    schedule=[["" for i in range(7)] for j in range(6)]
    adminSetting=AdminSetting.objects.all()[0]
    school_year=adminSetting.school_year
    school_term=adminSetting.school_term
    take_course=teacher.course_set.filter(start_year=school_year,course_id__course_term=school_term)
    for item in take_course:
        class_time=item.class_time.all()
        for t in class_time:
            schedule[t.category%10-1][t.category/10-1]+=item.course_id.course_name+"<br/>"+u"地点："+item.class_place.room_name+"<br/>"+u"上课周："+item.get_class_week_display()+"<br/>"
    context={"schedule":schedule}
    return render(request,"teacher/schedule.html",context)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def practiceclassViews(request,grade=None):
    teacher =request.user.teacherprofile_set.all()[0]
    smallclass=teacher.small_class
    year=getYearbyGrade(grade)
    practicelist=PracticeClassPractice.objects.filter(student__small_class=smallclass,student__innovation_grade=year)
    studentlist=[]
    a=["",u"一",u"二",u"三",u"四",u"五",u"六",u"日"]
    for item in practicelist:
        first=None
        second=None
        field_name='class_select_%d_%d'
        for i in range(1,8):
            for j in range(1,7):
                if getattr(item,field_name%(i,j)):
                    if(first==None):
                        first=u"周"+a[i]+u"第"+a[j]+u"大节"
                    else:
                        second=u"周"+a[i]+u"第"+a[j]+u"大节"
        if first!=None:
            studentlist.append({
                "student":item.student,
                "practice1":first,
                "practice2":second
            })
                
    context={"studentlist":studentlist}
    return render(request,"teacher/practiceclasslist.html",context)
