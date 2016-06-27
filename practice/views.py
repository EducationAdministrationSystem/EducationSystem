#encoding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse 
from common.models import Course,CoursePlan,SelectCourse
from users.models import PracticeProfile,TeacherProfile
from common.views import common_selfinfoViews, common_modifyPasswordViews
from django.http import HttpResponseRedirect,HttpResponse
from common.views import common_classchangeViews,common_studentmanageViews,common_studentsearchViews,common_selfinfoViews
from users.models import PracticeProfile
from users.models import ApplyInfo, PracticeProfile
import datetime
from common.forms import SmallClassForm,CoursePlanForm
from backend.decorators import *
from backend.utility import getContext
@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def selfinfoViews(request):
    cla = PracticeProfile.objects.get(userid = request.user)
    return render(request,"practice/self_info.html",{"full_name":cla.full_name,"nick_name":cla.nick_name})


@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def modifyPasswordViews(request):


    context = {
        'modify_password_info':common_modifyPasswordViews(request),

    }
    return render(request,"practice/modify_password.html",context)


@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def check_commentViews(request):
    practice = PracticeProfile.objects.get(userid = request.user)
    courselist = Course.objects.filter(course_id__course_practice=practice) 
    context = {
        'course_list':courselist,
    }
    return render(request, "practice/check_comment.html", context)
@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def studentmanageViews(request):
    context = common_studentmanageViews(request)
    return render(request,"practice/studentmanage/studentmanage_add.html",context)

@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def studentmanageSearchViews(request):
    context = common_studentsearchViews(request)
    return render(request,"practice/studentmanage/studentmanage_search.html",context)

@login_required
@authority_required(PRACTICE_USER)
def teachermanage(request):
    classlist = request.user.practiceprofile_set.all()[0].smallclass_set.all()
    context = {}
    for cla in classlist:
        context[cla.class_name] = cla.teacherprofile_set.all()
    context ={
        "class_teacher_list":context,
    }
    return render(request,"practice/teachermanage/teachermanage.html",context)

@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def studentselfinfoViews(request,sid = None):
    context = common_selfinfoViews(request,sid)
    return render(request,"practice/studentmanage/studentmanage_selfinfo.html",context)

@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def coursePlanViews(request):
    practice=PracticeProfile.objects.get(userid=request.user)
    course_plan_form=CoursePlanForm()
    context={
        "course_plan_list":practice.courseplan_set.all(),
        "course_plan_form":course_plan_form
    }
    return render(request,"practice/course_plan.html",context)
@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def recruitEntryViews(request):
    form = SmallClassForm(request = request)
    return render(request, "practice/recruit_entry.html", {"form": form, })

@csrf.csrf_protect
@login_required
@authority_required(PRACTICE_USER)
def courseViews(request):
    practice = PracticeProfile.objects.get(userid = request.user)
    course_list = Course.objects.filter(course_id__course_practice = practice)
    context =  getContext(course_list, 1, "item")
    context["show_delete"]=False
    return render(request,"practice/course_info.html",context)
def refresh_course_table(page=1):
    course = Course.objects.all()
    context =  getContext(course, page, "item")
    return render_to_string("widgets/course/course_table.html",
                                context)
