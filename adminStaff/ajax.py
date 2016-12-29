# coding=utf-8
import types
from dajax.core import Dajax
from django.contrib.auth.models import User
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.views.decorators import csrf
from django.utils import simplejson
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponseRedirect
from backend.utility import getContext
from backend.logging import loginfo
from django.db.models import Q
from adminStaff.forms import CourseForm,classRoomAddForm,ImportDataForm
from teacher.forms import TeacherAddForm,TeacherSearchForm
from common.forms import CourseFilterForm
from users.models import StudentProfile,SmallClass,TeacherProfile,PracticeProfile
from common.utility import create_student,isstudentExist,create_teacher,isteacherExist,delete_teacher
from common.utility import isClassExisted,create_class,isSmallClassExisted,create_smallclass
from common.utility import isClassRoomExist,create_classroom
from adminStaff.utility import get_xls_path
from common.models import Course,SelectCourse,CoursePlan, SmallClassPractice,PracticeClassPractice
from users.models import StudentProfile,SmallClass
from common.utility import create_student,isstudentExist,refresh_table
from teacher.forms import SmallClassForm
from adminStaff.views import getNextTerm
from const.models import AdminSetting,SchoolYear,ClassRoom
from practice.form import ClassAddForm,SmallClassAddForm


@dajaxice_register
def AddTeacher(request,form):
    teacher_form =TeacherAddForm(deserialize_form(form))
    if teacher_form.is_valid():
        data = teacher_form.cleaned_data
        name = data['baseinfo_name']
        teacherid = data['baseinfo_teacherid']
        smallclass = data['small_class']
        if not isteacherExist(teacherid.strip()):
            create_teacher(name,teacherid,smallclass)
            message ='人员添加成功'
            status ='1'
        else:
            print "hello"
            message ='教师已存在'
            status ='0'
        ret = {'status':status,'message':message,}
    else:
        return simplejson.dumps({'status':"2",'message':'输入有误，请重新输入','error_id': teacher_form.errors.keys(),})
    return  simplejson.dumps(ret)

@dajaxice_register
def SearchTeacher(request,form):
    teacher_form = TeacherSearchForm(deserialize_form(form))
    if teacher_form.is_valid():
        data = teacher_form.cleaned_data
        name = data['baseinfo_name'].strip()
        teacherid = data['baseinfo_teacherid'].strip()
        smallclass = data['small_class'].strip()
        q0=(name and Q(teacher_name=name)) or None
        q1=(teacherid and Q(teacher_id=teacherid)) or None
        q2=(smallclass and Q(small_class=smallclass)) or None
        qset = filter(lambda x:x!=None,[q0,q1,q2])
        if qset:
            qset=reduce(lambda x,y:x&y,qset)
            teacherlist = TeacherProfile.objects.filter(qset)
        else:
            teacherlist = TeacherProfile.objects.all()
        teacherlist_html = render_to_string('widgets/teacherlist.html',{'teacherlist':teacherlist})
        context={
            'teacherlist_html':teacherlist_html,
        }
    return simplejson.dumps(context)

@dajaxice_register
def DeleteTeacher(request,teacherid):
    if isteacherExist(str(teacherid.strip())):
        delete_teacher(teacherid)
        message = u'删除成功'
    else:
        message = u'教师不存在'
    teacherlist=TeacherProfile.objects.all()
    teacherlist_html = render_to_string('widgets/teacherlist.html',{'teacherlist':teacherlist})
    context={
        'teacherlist_html':teacherlist_html,
        'message':message,
    }
    return simplejson.dumps(context)


@dajaxice_register
def DetailTeacher(request,teacherid):
    teacher = TeacherProfile.objects.get(teacher_id=teacherid)
    detail_html = render_to_string("widgets/teacher_info.html",{'teacher':teacher})
    context={
        'detail_html':detail_html,
    }
    return simplejson.dumps(context)

@dajaxice_register
def getEditTeacherForm(request,teacherid):
    teacher = TeacherProfile.objects.get(teacher_id=teacherid)
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
        'teacherid':teacherid,
    }
    return simplejson.dumps(context)

@dajaxice_register
def EditTeacher(request,form,teacherid):
    editform = TeacherAddForm(deserialize_form(form))
    if editform.is_valid():
        data = editform.cleaned_data
        teacher = TeacherProfile.objects.get(teacher_id=teacherid)
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
        print "---------------------------"
        print editform.errors
        message="请正确输入信息"
    teacherlist = TeacherProfile.objects.all()
    teacherlist_html = render_to_string('widgets/teacherlist.html',{'teacherlist':teacherlist})
    context={
        'message':message,
        'teacherlist_html':teacherlist_html,
    }
    return simplejson.dumps(context)


@dajaxice_register
@csrf.csrf_protect
def CourseInfo(request,filter_form,form,uid,page):
    if uid == 0:
        courseForm = CourseForm(deserialize_form(form))
    else:
        course = Course.objects.get(id=uid)
        courseForm = CourseForm(deserialize_form(form),instance=course)
    if courseForm.is_valid():
        courseForm.save()
        table=refresh_course_table(filter_form,page)
        courseForm = CourseForm()
        form_html = render_to_string("widgets/course/course_form.html",{'course_form':courseForm})
        return simplejson.dumps({ 'status':'1', 'message':u"课程信息添加成功",'table':table,'form':form_html})
    else:
        form_html = render_to_string("widgets/course/course_form.html",{'course_form':courseForm})
        return simplejson.dumps({ 'status':'0', 'message':u"输入有误",'form':form_html})

@dajaxice_register
@csrf.csrf_protect
def GetCourseForm(request,uid):
    if uid == 0:
        courseForm = CourseForm()
    else:
        course = Course.objects.get(id=uid)
        courseForm = CourseForm(instance=course)
    form_html = render_to_string("widgets/course/course_form.html",{'course_form':courseForm})
    return simplejson.dumps({'form':form_html})

@dajaxice_register
def CoursePagination(request,filter_form,page):
    table = refresh_course_table(filter_form,page)
    return simplejson.dumps({ 'status':'2', 'table':table})

@dajaxice_register
def DeleteCourse(request,filter_form,uid,page):
    try:
        print uid
        course = Course.objects.get(id=uid)
        course.delete()
        table=refresh_course_table(filter_form,page)
        return simplejson.dumps({ 'status':'1', 'message':u"删除成功",'table':table})
    except Exception,e:
        print e
        return simplejson.dumps({ 'status':'3', 'message':u"删除条目不存在"})

def get_filter_data(filter_form):
    course_filter_form = CourseFilterForm(deserialize_form(filter_form))
    if course_filter_form.is_valid():
        classes = course_filter_form.cleaned_data['classes']
        terms   = course_filter_form.cleaned_data['terms']
        grades  = course_filter_form.cleaned_data['grades']
        years   = course_filter_form.cleaned_data['years']
        if classes == '-1':
            classes = ''
        if  terms == '-1':
            terms = ''
        if  grades == '-1':
            grades = ''
        if  years== '-1':
            years = ''
        q0 = (classes and Q(course_id__course_practice__nick_name = classes)) or None
        q1 = (terms   and Q(course_id__course_term = terms)) or None
        q2 = (grades  and Q(course_id__course_grade = grades)) or None
        q3 = (years   and Q(start_year = years)) or None
        qset=filter(lambda x:x!=None,[q0,q1,q2,q3])
        if qset:
            qset=reduce(lambda x,y: x&y ,qset)
            course_list= Course.objects.filter(qset)
        else:
            course_list= Course.objects.all()
        return course_list
    course_list= Course.objects.all()
    return course_list
def refresh_course_table(filter_form,page=1):
    course = get_filter_data(filter_form)
    context =  getContext(course, page, "item")
    context["show_delete"]=True
    return render_to_string("widgets/course/course_table.html",
                                context)
@dajaxice_register
@csrf.csrf_protect
def exportSearchCourse(request,filter_form):
    course_set = get_filter_data(filter_form)
    head_dict = [u'课名',u'课程号',u'教师',u'上课周',u'上课时间',u'上课地点',u'总学时',u'实践学时',u'理论学时',u'课容量',u'已选人数',u'学分',u'年级',u'学年',u'学期',u'实践班']
    excelname = u"课程时间表"
    path = get_xls_path(request,head_dict,course_set,excelname)
    return simplejson.dumps({'path':path})
@dajaxice_register
@csrf.csrf_protect
def getSmallClass(request, smallClassId):
    smallClassPractice = SmallClassPractice.objects.get(id = smallClassId)
    small_class=smallClassPractice.small_class.brother_class
    smallClassPractice_b=SmallClassPractice.objects.get(small_class=small_class,class_grade=smallClassPractice.class_grade)
    context = {}
    smallClassForm = SmallClassForm(instance = smallClassPractice_b)
    context["smallClassForm"] = smallClassForm
    return render_to_string("adminStaff/widgets/classRemainTable.html",
                                context)

@dajaxice_register
@csrf.csrf_protect
def updateSmallClass(request, form, smallClassId):
    smallClassPractice = SmallClassPractice.objects.get(id = smallClassId)
    small_class=smallClassPractice.small_class.brother_class
    smallClassPractice_b=SmallClassPractice.objects.get(small_class=small_class,class_grade=smallClassPractice.class_grade)
    loginfo(smallClassPractice)
    smallClassForm = SmallClassForm(deserialize_form(form), instance = smallClassPractice_b)
    if smallClassForm.is_valid():
        print "small class update form is valid"
        smallClassForm.save()
    else: print "small class update form is not valid!"
    context = {}
    context["smallClassForm"] = smallClassForm
    return render_to_string("adminStaff/widgets/classRemainTable.html",
                                context)

def ClearSmallPractice():
    small_class_practice=SmallClassPractice.objects.all()
    for scp in small_class_practice:
        for i in range(1,8):
            for j in range(1,7):
                remainFieldName="class_remain_%d_%d"%(i,j)
                setattr(scp,remainFieldName,0)
        scp.save()

@dajaxice_register
def GoNextTerm(request,first):
    adminSetting=AdminSetting.objects.all()[0]
    school_year=adminSetting.school_year.school_year
    school_term=adminSetting.school_term
    next_year,next_term=getNextTerm(school_year,school_term)
    next_year_object,created=SchoolYear.objects.get_or_create(school_year=next_year)
    next_year_object.save()
    adminSetting.school_year=next_year_object
    adminSetting.tearm_first_day=first
    adminSetting.school_term=next_term
    adminSetting.course_select_start=None
    adminSetting.course_select_end=None
    adminSetting.score_enter_start=None
    adminSetting.score_enter_end=None
    adminSetting.save()
    ClearSmallPractice()
    practice_all=PracticeClassPractice.objects.all()
    practice_all.delete()
    return simplejson.dumps({})

@dajaxice_register
def SetCourseTime(request,start,end):
    adminSetting=AdminSetting.objects.all()[0]
    adminSetting.course_select_start=start
    adminSetting.course_select_end=end
    adminSetting.save()
    return simplejson.dumps({})
@dajaxice_register
def SetScoreTime(request,start,end):
    adminSetting=AdminSetting.objects.all()[0]
    adminSetting.score_enter_start=start
    adminSetting.score_enter_end=end
    adminSetting.save()
    return simplejson.dumps({})
@dajaxice_register
def CourseSelectSwitch(request):
    adminSetting=AdminSetting.objects.all()[0]
    adminSetting.course_select_switch=not adminSetting.course_select_switch
    adminSetting.save()
    return simplejson.dumps({})
@dajaxice_register
def ClassChangeSwitch(request):
    adminSetting=AdminSetting.objects.all()[0]
    adminSetting.class_change_switch=not adminSetting.class_change_switch
    adminSetting.save()
    return simplejson.dumps({})

@dajaxice_register
def RecruitSwitch(request):
    adminSetting=AdminSetting.objects.all()[0]
    print "111111",adminSetting.recruit_switch
    adminSetting.recruit_switch=not adminSetting.recruit_switch
    print "222222",adminSetting.recruit_switch
    adminSetting.save()
    return simplejson.dumps({})

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
def AddClass(request,form):
    form = ClassAddForm(deserialize_form(form))
    if form.is_valid():
        data = form.cleaned_data
        full_name = data['fullname'].strip()
        nick_name = data['nickname'].strip()
        if not isClassExisted(full_name,nick_name):
            create_class(full_name,nick_name)
            message="添加成功"
        else:
            message="班级已存在"
    else:
        message="输入有误"
    classlist = PracticeProfile.objects.all()
    classlist_html = render_to_string("widgets/classlist.html",{'classlist':classlist})
    return simplejson.dumps({"classlist_html":classlist_html,'message':message})

@dajaxice_register
def AddSmallClass(request,form):
    form = SmallClassAddForm(deserialize_form(form))
    if form.is_valid():
        data = form.cleaned_data
        class_name = data['class_name'].strip()
        practice_class = data['practice_class'].strip()
        loginfo(practice_class)
        if not isSmallClassExisted(class_name,practice_class):
            create_smallclass(class_name,practice_class)
            message="添加成功"
        else:
            message="班级已存在"
    else:
        message="输入有误"
    return simplejson.dumps({"message":message})

@dajaxice_register
def DeleteClass(request,classid):
    print "+++++++++++++++++++++++++++++++++++"
    cla = PracticeProfile.objects.get(id = classid)
    cla.userid.delete()
    classlist =PracticeProfile.objects.all()
    classlist_html = render_to_string("widgets/classlist.html",{'classlist':classlist})
    return simplejson.dumps({"classlist_html":classlist_html})

@dajaxice_register
def ChosePractice(request,pid):
    pid=int(pid)
    context={
        "course_plan_list":CoursePlan.objects.filter(course_practice=pid)
    }
    courseplan_html=render_to_string("widgets/course_plan_table.html",context)
    return simplejson.dumps({"courseplan_html":courseplan_html})



@dajaxice_register
def ChoseRoom(request,rid):
    room=ClassRoom.objects.get(pk=rid)
    schedule=[["" for i in range(7)] for j in range(6)]
    adminSetting=AdminSetting.objects.all()[0]
    school_year=adminSetting.school_year
    school_term=adminSetting.school_term
    take_course=room.course_set.filter(start_year=school_year,course_id__course_term=school_term)
    print take_course.count()
    for item in take_course:
        class_time=item.class_time.all()
        for t in class_time:
            schedule[t.category%10-1][t.category/10-1]+="<br/>"+item.course_id.course_name+"<br/>"+u"上课老师："+item.teacher.teacher_name+"<br/>"+u"上课周："+item.get_class_week_display()
    context={"schedule":schedule}
    roomhtml=render_to_string("adminStaff/widgets/classroom_schedule.html",context)
    return simplejson.dumps({"roomhtml":roomhtml})

@dajaxice_register
def AddClassRoom(request,form):
    classroom =classRoomAddForm(deserialize_form(form))
    if classroom.is_valid():#在这里已判断是否已经存在这个教室
        name = classroom.cleaned_data['room_name']
        create_classroom(name)
        ret = {'message':'添加成功'}
    else:
        ret = {'message':'教室已存在'}
    return  simplejson.dumps(ret)

@dajaxice_register
def CourseStatistical(request,rid):
    rid=int(rid)
    terms=[]
    small_class=SmallClass.objects.all()
    for i in xrange(3):
        year=(str(rid+i)+"-"+str(rid+1+i))
        school_year,u=SchoolYear.objects.get_or_create(school_year=year)
        terms.append({
            "school_year":school_year,
            "term":(1,u"秋季"),
            "grade":i+1,
            "count":0
        })
        terms.append({
            "school_year":school_year,
            "term":(2,u"春季"),
            "grade":i+1,
            "count":0
        })

    statistical=[]

    selectors=[]
    Quanxiao=PracticeProfile.objects.filter(nick_name="qyggk")[0]
    for term in terms:
        courses=Course.objects.filter(start_year=term['school_year'],course_id__course_term=term["term"][0],course_id__course_practice=Quanxiao,course_id__course_grade=term["grade"])
        people=0
        for c in courses:
            people=people+c.int_nelepeo
        selectors.append(people)
    statistical.append({
        "name":u"公共课程",
        "selectors":selectors
    })
    for item in small_class:
        selectors=[]
        for term in terms:
            courses_select=SelectCourse.objects.filter(course__course_to_class=item,course__start_year=term["school_year"],course__course_id__course_term=term["term"][0],course__course_id__course_practice=item.practice_class,course__course_id__course_grade=term["grade"],student__small_class=item)
            people=courses_select.count()
            #for c in courses_select:
                #people=people+c.count()
            term["count"]+=people
            selectors.append(people)
        statistical.append({
            "name":item.class_name,
            "selectors":selectors
        })
        html=render_to_string("adminStaff/widgets/statistical_table.html",{"terms":terms,"statistical":statistical})
    return simplejson.dumps({"html":html})
