# Create your views here.
#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from teacher.forms import TeacherAddForm,TeacherSearchForm
from practice.form import ClassAddForm
from adminStaff.forms import classRoomAddForm
from users.models import StudentProfile,TeacherProfile,PracticeProfile
from student.models import ChangeClassApply
from student.forms import StudentInfoForm,StudentAddForm,StudentSearchForm,ClassChangePreviewForm
from users.models import StudentProfile,TeacherProfile
from backend.logging import loginfo
from django.db.models import Q
from const import *
from backend.utility import getContext
from django.contrib.auth.models import User
def common_modifyPasswordViews(request):

    user =  User.objects.get(id = request.user.id)
    if request.method == "POST":
        new = request.POST['input_new_password']
        repeat = request.POST['repeat_new_password']
        if new != repeat:
            return u"输入密码不一致！"
        elif new == "":
            return u"输入密码为空！"
        else:
            user.set_password(request.POST['input_new_password'])
            user.save()
            return u"修改密码成功！"
    else :
        return u""

def common_selfinfoViews(request,sid = None):
    student = StudentProfile.objects.get(baseinfo_studentid = sid)
    issave = False
    role = request.session.get('auth_role', "")
    if request.method == 'POST':
        infoform = StudentInfoForm(request.POST,instance = student)
        if infoform.is_valid():
            infoform.save()
            issave = True
        else:
            print infoform.errors
    else:
        infoform = StudentInfoForm(instance = student)
    context = {
        "infoform":infoform,
        "student":student,
        "isSave":issave,
        "role":role,
    }
    return context
def common_studentmanageViews(request):
    addform = StudentAddForm(request = request);
    context = {
        'addform':addform,
    }
    return context

def common_teachermanageViews(request):
    addform = TeacherAddForm()
    context = {
        'addform':addform,
    }
    return context

def common_classmanageview(request):
    classlist = PracticeProfile.objects.all()
    classAddForm = ClassAddForm()
    context ={
        "classlist":classlist,
        "classAddForm":classAddForm,
    }
    return context


def common_getTeacherInfoViews(request):
    searchform = TeacherSearchForm();
    teacherlist = TeacherProfile.objects.all()
    context = {
        'teacherlist':teacherlist,
        'searchform':searchform,
        }
    return context

def common_studentsearchViews(request):
    role = request.session.get('auth_role', "")
    stu_set = ""
    if request.method == 'POST':
        searchform = StudentSearchForm(request.POST,request = request)
        stu_set = stuFilterList(request,searchform).order_by("small_class","innovation_grade")
    else:
        searchform = StudentSearchForm(request = request)
    context = getContext(stu_set,1,"item",0)
    context.update({
        'searchform':searchform,
        'role':role,
    })
    return context

def stuFilterList(request,searchform):
    if searchform.is_valid():
        practice_class = searchform.cleaned_data["practice_class"]
        small_class =  searchform.cleaned_data["small_class"]
        innovation_grade = searchform.cleaned_data["innovation_grade"]
        baseinfo_name_studentid = searchform.cleaned_data["baseinfo_name_studentid"]
        qset = get_filter(practice_class,small_class,innovation_grade,baseinfo_name_studentid)
        if qset :
            qset = reduce(lambda x, y: x & y, qset)
            stu_list = StudentProfile.objects.filter(qset)
        else:
            stu_list = StudentProfile.objects.all()
    else:
        print searchform.errors
    return stu_list

def get_filter(practice_class,small_class,innovation_grade,baseinfo_name_studentid):
    if practice_class == "-1":
        practice_class=''
    if small_class == '-1':
        small_class=''
    if innovation_grade == '-1':
        innovation_grade=''

    q1 = (practice_class and Q(small_class__practice_class=practice_class)) or None
    q2 = (small_class and Q(small_class=small_class)) or None
    q3 = (innovation_grade and Q(innovation_grade=innovation_grade)) or None
    q4 = (baseinfo_name_studentid and (Q(baseinfo_name__contains = baseinfo_name_studentid) | Q(baseinfo_studentid__contains = baseinfo_name_studentid))) or None
    qset = filter(lambda x: x != None, [q1, q2, q3,q4])
    return qset

def common_classchangeViews(request,teachertype = None):
    role = request.session.get('auth_role', "")
    if role == "adminStaff":
        change_role = "dean"
        changeclass_set = ChangeClassApply.objects.filter(originOK = AGREE_CHOICE_AGREE,receiveOK = AGREE_CHOICE_AGREE,deanOK = AGREE_CHOICE_UNDFINED)
        changeclasshandled_set = ChangeClassApply.objects.exclude(deanOK = AGREE_CHOICE_UNDFINED)
    elif role == "teacher":
        teacher = TeacherProfile.objects.get(userid = request.user)
        if teachertype == "origin":
            change_role = "origin"
            changeclass_set = ChangeClassApply.objects.filter(originclass = teacher.small_class, originOK = AGREE_CHOICE_UNDFINED)
            changeclasshandled_set = ChangeClassApply.objects.filter(originclass = teacher.small_class).exclude(originOK = AGREE_CHOICE_UNDFINED)
        else:
            change_role = "receive"
            applyAll = ChangeClassApply.objects.all()
            print "################"
            print len(applyAll)
            changeclass_set = ChangeClassApply.objects.filter(receiveclass = teacher.small_class, originOK = AGREE_CHOICE_AGREE,receiveOK = AGREE_CHOICE_UNDFINED)
            print len(changeclass_set)
            changeclasshandled_set = ChangeClassApply.objects.filter(receiveclass = teacher.small_class).exclude(receiveOK = AGREE_CHOICE_UNDFINED)
            print "*********"
            print len(changeclasshandled_set)
    changepreviewform = ClassChangePreviewForm()
    context = {
        'changeclass_set':changeclass_set,
        'changeclasshandled_set':changeclasshandled_set,
        'changepreviewform':changepreviewform,
        'change_role':change_role,
    }
    return context

def common_classRoomAddView(request):
    form = classRoomAddForm()
    context = {
        'addform':form,
    }
    return context
