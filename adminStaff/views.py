# Create your views here.
#coding=utf-8
from settings import TMP_FILES_PATH,MEDIA_URL
import json
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse
from common.views import common_teachermanageViews,common_getTeacherInfoViews,common_studentmanageViews
from common.views import common_studentsearchViews,common_selfinfoViews,common_classchangeViews
from common.views import common_classmanageview,common_classRoomAddView
from django.db.models.loading import get_model
from django.views.decorators import csrf
from common.views import common_selfinfoViews, common_modifyPasswordViews
from backend.logging import loginfo
from backend.utility import getContext
from common.models import Course
from adminStaff.forms import CourseForm, SmallClassSelectForm,PracticeSelectForm,ClassRoomForm,ImportDataForm,GradeYearForm
from adminStaff.utility import xls_import_course
from backend.decorators import *
from const.models import AdminSetting
from const import TERM_CHOICE
from common.forms import CourseFilterForm, StudentFilterForm,CoursePlanForm
from practice.form import SmallClassAddForm
from users.models import StudentProfile
@authority_required(ADMINSTAFF_USER)
def homeviews(request):
    return render(request,"adminStaff/adminStaff_home.html")

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def modifyPasswordViews(request):

    context = {
        'modify_password_info':common_modifyPasswordViews(request),
    }
    return render(request,"adminStaff/modify_password.html",context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def modifyStudentPasswordViews(request):

    modify_password_info = u""
    if request.method == "POST":
        student_id = request.POST['input_student_id']
        new = request.POST['input_new_password']
        repeat = request.POST['repeat_new_password']

        student = StudentProfile.objects.filter(baseinfo_studentid = student_id)
        if not student:
            modify_password_info = u"没有查到有此学号的学生!"
        else:
            student = student[0]
            user =  User.objects.get(id = student.userid.id)
            if new != repeat:
                modify_password_info = u"输入密码不一致！"
            elif new == "":
                modify_password_info =  u"输入密码为空！"
            else:
                user.set_password(request.POST['input_new_password'])
                user.save()
                modify_password_info =  u"修改密码成功！"
    else :
        modify_password_info = u""

    context = {
        'modify_password_info':modify_password_info,

    }
    return render(request,"adminStaff/modify_student_password.html",context)

@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def courseViews(request):
    filterForm = CourseFilterForm()
    courseForm = CourseForm()
    importDataForm = ImportDataForm()
    course_list = Course.objects.all()
    context =  getContext(course_list, 1, "item")
    context['course_form']= courseForm
    context['importDataForm']=importDataForm
    context["show_delete"]=True
    context["filter_form"]=filterForm
    return render(request,"adminStaff/course/course_info.html",context)
def refresh_course_table(page=1):
    course = Course.objects.all()
    context =  getContext(course, page, "item")
    context["show_delete"]=True
    return render_to_string("widgets/course/course_table.html",
                                context)
@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def importCourseData(request):
    if request.is_ajax():
        form = ImportDataForm(request.POST,request.FILES)
        if form.is_valid():
            doc = form.cleaned_data['document']
            save_path = os.path.join(TMP_FILES_PATH,'upload/',doc.name )
            fp = file(save_path,'wb')
            fp.write(doc.read())
            fp.close()
            ret = xls_import_course(save_path)
            if ret[0]==True:
                table= refresh_course_table()
                return HttpResponse(json.dumps({'status':'1','message':u'导入成功','table':table}),content_type = "application/json")
            return HttpResponse(json.dumps({'status':'0','message':u'导入失败','path':ret[1].replace(TMP_FILES_PATH,MEDIA_URL+"tmp")}),content_type = "application/json")
@login_required
@authority_required(ADMINSTAFF_USER)
def courseExportViews(request):
    return render(request,"adminStaff/course/course_export.html")

@login_required
@authority_required(ADMINSTAFF_USER)
def studentmanageViews(request):
    context = common_studentmanageViews(request)
    return render(request,"adminStaff/studentmanage/studentmanage_add.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
def studentmanage_searchViews(request):
    context = common_studentsearchViews(request)
    return render(request,"adminStaff/studentmanage/studentmanage_search.html",context)

@login_required
@csrf.csrf_protect
@authority_required(ADMINSTAFF_USER)
def selfinfoViews(request,sid = None):
    context = common_selfinfoViews(request,sid)
    return render(request,"adminStaff/studentmanage/studentmanage_selfinfo.html",context)

def getNextTerm(year,term):
    if term==1:
        return (year,2)
    else:
        froYear=str(int(year[:4])+1)
        aftYear=str(int(year[-4:])+1)
        return (froYear+"-"+aftYear,1)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def teachermanageViews(request):
	context = common_teachermanageViews(request)
	return render(request,"adminStaff/teachermanage/teachermanage_add.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def teachermanage_searchViews(request):
	context = common_getTeacherInfoViews(request)
	return render(request,"adminStaff/teachermanage/teachermanage_search.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def studentmanage_classchangeViews(request):
    context = common_classchangeViews(request)
    return render(request,"adminStaff/studentmanage/studentmanage_classchange.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def studentmanage_studentchangeclassViews(request):
    return render(request,"adminStaff/studentmanage/studentmanage_studentchangeclass.html")

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def managementSettingViews(request):
    adminSetting=AdminSetting.objects.all()[0]
    school_year=adminSetting.school_year.school_year
    school_term=adminSetting.school_term
    next_year,next_term=getNextTerm(school_year,school_term)
    course_start=adminSetting.course_select_start
    course_end=adminSetting.course_select_end
    score_start=adminSetting.score_enter_start
    score_end=adminSetting.score_enter_end
    course_select_switch=adminSetting.course_select_switch
    class_change_switch=adminSetting.class_change_switch
    recruit_switch=adminSetting.recruit_switch
    context={
        "cur_year":school_year,
        "cur_term":TERM_CHOICE[school_term][1],
        "next_year":next_year,
        "next_term":TERM_CHOICE[next_term][1],
        "course_start":course_start,
        "course_end":course_end,
        "score_start":score_start,
        "score_end":score_end,
        "course_select_switch":course_select_switch,
        "class_change_switch":class_change_switch,
        "recruit_switch":recruit_switch
    }
    return render(request,"adminStaff/management_setting.html",context)


@csrf.csrf_protect
@login_required
@authority_required(ADMINSTAFF_USER)
def classRemainViews(request, smallClass = 1):
    context = {}
    context["classChoice"] = SmallClassSelectForm()
    return render_to_response("adminStaff/classRemain.html", context, context_instance = RequestContext(request))


@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def studentListQueryViews(request):
    form = StudentFilterForm()
    context = {
            "form": form,
        }
    return render(request, "adminStaff/student_list_query.html", context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def studentScoreSearchViews(request):
    context = {}
    return render(request, "adminStaff/student_score_search.html", context)
@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def scoreListQueryViews(request):
    form = CourseFilterForm()
    context = {
            "form": form,
        }
    return render(request, "adminStaff/score_list_query.html", context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def classListQueryViews(request):
    form = CourseFilterForm()
    context = {
            "form": form,
    }
    return render(request, "adminStaff/class_list_query.html", context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def admin_commentViews(request):
    course_all=Course.objects.all()
    course_list=[]
    for course in course_all:
        course_list.append(course)
    context={
        'course_list':course_list
    }
    return render(request,"adminStaff/admin_comment.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def classmanageViews(request):
    context = common_classmanageview(request)
    return render(request,"adminStaff/classmanage/classmanage.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def small_classViews(request):
    form=SmallClassAddForm()
    context ={
        'form':form
    }
    return render(request,"adminStaff/classmanage/small_class_manage.html",context)


@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def coursePlanViews(request):
    course_plan_form=CoursePlanForm()
    context={
        "classChoice" : PracticeSelectForm(),
        "course_plan_form":course_plan_form
    }
    return render(request,"adminStaff/course_plan.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def courseSelectViews(request):
    context={}
    return render(request,"adminStaff/course_select.html",context)

@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def courseDeleteViews(request):
    context={}
    return render(request,"adminStaff/delete_course.html",context)


@login_required
@authority_required(ADMINSTAFF_USER)
@csrf.csrf_protect
def classRoomViews(request):
    schedule=[["" for i in range(7)] for j in range(6)]
    context={
        "classroomChoice":ClassRoomForm(),
        "schedule":schedule
    }

    return render(request,"adminStaff/classroom/schedule.html",context)

@login_required
@csrf.csrf_protect
@authority_required(ADMINSTAFF_USER)
def classRoomAddViews(request):
    context = common_classRoomAddView(request)
    return render(request,"adminStaff/classroom/classRoomAdd.html",context)


@login_required
@csrf.csrf_protect
@authority_required(ADMINSTAFF_USER)
def courseStatisticalViews(request):
    context={
        'GradeYearForm':GradeYearForm()
    }
    return render(request,"adminStaff/course_statistical.html",context)
