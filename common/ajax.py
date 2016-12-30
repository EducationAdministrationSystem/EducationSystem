# coding: UTF-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.contrib.auth.models import User
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from users.models import StudentProfile,TeacherProfile,SmallClass
from student.models import ChangeClassApply
from common.utility import refresh_table,create_student,isstudentExist,selectCourseContext,AdminDeleteCourseContext
from common.views import common_classchangeViews,stuFilterList
from django.template.loader import render_to_string
from users.models import StudentProfile, TeacherProfile, PracticeProfile
from common.models import SelectCourse,Course, Score, SelectCourse,CoursePlan
from backend.logging import loginfo
from django.db.models import Q
from backend.decorators import check_auth
from const import *
from backend.utility import getContext
from student.forms import StudentSearchForm,StudentAddForm,studentchangeclassForm
from adminStaff.utility import get_xls_path,get_score_xls_path
from common.forms import CoursePlanForm

@dajaxice_register
def getCollege(request,apartment):
    apartment=int(apartment)
    college=COLLEGE_DICT.get(apartment,None)
    return simplejson.dumps({"college":college})


@dajaxice_register
def SelectCourseOperation(request,selected,sid):
    status=""
    if sid ==-1:
        student=StudentProfile.objects.get(userid=request.user)
    else:
        student=StudentProfile.objects.get(pk=sid)
    for item in selected:
        item=int(item)
        select_course=SelectCourse.objects.filter(student=student,course__pk=item)
        if select_course.count()==0:
            course=Course.objects.get(pk=item)
            if course.int_nelepeo == course.class_capacity:
                status=status+u"课程“"+course.course_id.course_name+u"” 已经没有课余量，选课失败！"+"<br/>"
            #!!!!!!
            # it should be rewrite later
            # elif checkTimeCrash(course,student):
            #     status=status+u"课程“"+course.course_id.course_name+u"” 与已选课程上课时间冲突，选课失败！"+"<br/>"
            #elif SelectCourse.objects.filter(student=student,course__course_id=course.course_id):
                #status=status+u"课程“"+course.course_id.course_name+u"” 相同课程计划课程已经选过，选课失败！"+"<br/>"
            else:
                course.int_nelepeo=course.int_nelepeo+1
                course.save()
                course_select_item=SelectCourse(student=student,course=course)
                course_select_item.save()
                Score(select_obj = course_select_item).save()

                status=status+u"课程“"+course.course_id.course_name+u"” 选课成功！"+"<br/>"
    return simplejson.dumps({"status":status})

@dajaxice_register
def change_apply_overstatus(request, apply_id, changed_overstatus,change_role):
    '''
    change project overstatus
    '''
    choices = dict(AGREE_CHOICE)
    changeapply = ChangeClassApply.objects.get(id = apply_id)
    if change_role == "dean":
        changeapply.deanOK = changed_overstatus
    elif change_role == "origin":
        changeapply.originOK = changed_overstatus
    elif change_role == "receive":
        changeapply.receiveOK = changed_overstatus
    changeapply.save()
    if change_role == "dean" and changeapply.deanOK:
        student = StudentProfile.objects.get(baseinfo_studentid = changeapply.student_id)
        student.small_class = changeapply.receiveclass
        student.innovation_grade=changeapply.innovation_grade
        student.save()


    context = common_classchangeViews(request,change_role)
    table_fre = refresh_table(request,"common/student/classchangetable.html",context)
    return simplejson.dumps({'status':'1', 'table_fre':table_fre})

def checkTimeCrash(course,student):
    select_course=student.selectcourse_set.all()
    for item in select_course:
        class_time=item.course.class_time.all()
        for t in class_time:
            for ct in course.class_time.all():
                if t==ct:
                    return True
    return False

@dajaxice_register
def DeleteCourseOperation(request,selected,sid):
    status=""
    if sid ==-1:
        student=StudentProfile.objects.get(userid=request.user)
    else:
        student=StudentProfile.objects.get(pk=sid)
    for item in selected:
        select_course=SelectCourse.objects.filter(student=student,course__pk=item)[0]
        course=Course.objects.get(pk=item)
        course.int_nelepeo=course.int_nelepeo-1
        course.save()
        select_course.delete()
        status=status+u"课程“"+course.course_id.course_name+u"” 删除成功！"+"<br/>"
    return simplejson.dumps({"status":status})

@dajaxice_register
def getCourseList(request, year, term, grade, page_numbers, cls, page):
    try:
        print "ddddddddddd"
        page = int(page)
        page_numbers = int(page_numbers)

        courses = Course.objects.all()
        if year != "-1": courses = courses.filter(start_year = year)
        if term != "-1": courses = courses.filter(course_id__course_term = term)
        if grade != "-1": courses = courses.filter(course_id__course_grade = grade)

        if check_auth(request.user, TEACHER_USER):
            teacher = TeacherProfile.objects.get(userid = request.user)
            courses = courses.filter(teacher = teacher)
        elif cls != "-1":
             courses = courses.filter(course_id__course_practice__userid__username = cls)

        context = getContext(courses, page, "item", 1, page_numbers)
        html = render_to_string("teacher/widgets/course_set_table.html", context)
    except Exception,e:
        print "aaaaaaaaa"
    return simplejson.dumps({"html": html, })

@dajaxice_register
def getCourseScores(request, course_id, page):
    page = int(page)
    selects = SelectCourse.objects.filter(course__id = course_id)
    for select in selects:
        tmp_score = Score.objects.filter(select_obj = select)
        if tmp_score:
            select.score = tmp_score[0]
        else :
            continue
        # select.score = Score.objects.get(select_obj = select)
    context = getContext(selects, page, "item2", 1)
    context.update({"course_id": course_id, })
    html = render_to_string("teacher/widgets/score_info_table.html", context)
    return simplejson.dumps({"html": html, })

@dajaxice_register
def exportSimpleCourseScores(request, course_id):
    course = Course.objects.get(id = course_id)
    selects = SelectCourse.objects.filter(course__id = course_id)
    # scores = [Score.objects.get(select_obj = select) for select in selects]
    scores = []
    for select in selects:
        tmp_score = Score.objects.filter(select_obj = select)
        if tmp_score:
            scores.append(tmp_score[0])
        else:
            continue
    head_dict = {0:u'姓名',1:u'分数',}
    excelname = course.course_id.course_name + u"学生成绩汇总"
    return get_xls_path(request,head_dict,scores,excelname, "get_simple_export_data")

@dajaxice_register
def exportAll(request):
    head_dict = [u'学号', u'姓名', u'课程号', u'课程名', u'开课年',u'开课学期', u'成绩', ]
    excelname = u"学生成绩汇总"
    scores = Score.objects.all()
    return get_xls_path(request, head_dict, scores, excelname, "get_all_data")

@dajaxice_register
def exportCourseScores(request, course_id):
    course = Course.objects.get(id = course_id)
    selects = SelectCourse.objects.filter(course__id = course_id)
    smallclass = course.course_id.course_practice.full_name
    classnum = course.course_id.course_plan_id
    coursename = course.course_id.course_name
    startyear = course.start_year.school_year
    courseterm = course.course_id.get_course_term_display()
    teacher = course.teacher.teacher_name
    point = course.course_id.course_point
    excelhead =[smallclass,classnum,coursename,startyear,courseterm,teacher,point,4]

    # scores = [Score.objects.get(select_obj = select) for select in selects]
    scores = []
    for select in selects:
        tmp_score = Score.objects.filter(select_obj = select)
        if tmp_score:
            scores.append(tmp_score[0])
        else:
            continue
    count = [0,0,0,0,0,0,0,0]
    total = 0
    for item in scores:
        score = item.total
        if score >=90 and score <=100:
            count[0] +=1
        elif score >=80 and score <90:
            count[1] +=1
        elif score >=70 and score <89:
            count[2] +=1
        elif score >=60 and score <79:
            count[3] +=1
        elif score >=0 and score <60:
            count[4] +=1
        else:
            count[6] +=1
        total += score
        count[7] +=1
    count[5] = total / float(count[7])
    count[5] = round(count[5],1)
    #head_dict = [u'姓名', u'学号', u'院系', u'考勤分数', u'平时作业', u'期末评测', u'总分',]
    head_dict = [u'顺序', u'学号', u'姓名', u'院系', u'成绩', u'顺序', u'学号', u'姓名', u'院系', u'成绩']
    excelname = u"大连理工大学考核成绩登记表"

    return get_score_xls_path(request,head_dict,scores,excelname,"get_export_data",excelhead,count)


@dajaxice_register
def getCourseMembers(request, course_id, page):
    page = int(page)
    selects = SelectCourse.objects.filter(course__id = course_id)
    context = getContext(selects, page, "item2", 1)
    context.update({"course_id": course_id, })
    html = render_to_string("teacher/widgets/course_info_table.html", context)
    return simplejson.dumps({"html": html, })

@dajaxice_register
def exportCourseMembers(request, course_id):
    course = Course.objects.get(id = course_id)
    selects = SelectCourse.objects.filter(course__id = course_id)
    stu_set = [select.student for select in selects]
    head_dict = {0:u'姓名',1:u'学号',2:u'所属班级',3:u'进入年份',4:u'性别',5:u'院系',6:u'邮箱',7:u'电话'}
    excelname = course.course_id.course_name + u"学生信息表"
    return get_xls_path(request,head_dict,stu_set,excelname)



@dajaxice_register
def searchStudent(request, search_value):
    students = StudentProfile.objects.filter(Q(baseinfo_name = search_value) | Q(baseinfo_studentid = search_value))
    if check_auth(request.user, TEACHER_USER):
        teacher = TeacherProfile.objects.get(userid = request.user)
        students = students.filter(small_class = teacher.small_class)
    context = getContext(students, 1, "item", 0)
    return render_to_string("teacher/widgets/student_set_table.html", context)

@dajaxice_register
def getSearchChangeClassStudent(request, search_value):
    students = StudentProfile.objects.filter(Q(baseinfo_name = search_value) | Q(baseinfo_studentid = search_value))
    if students:
        student = students[0]
        studentchangeclass = studentchangeclassForm(studentname=student.baseinfo_name,
            studentid=student.baseinfo_studentid,
            originclass=student.small_class.class_name)
    else:
        studentchangeclass = studentchangeclassForm(studentname="",
            studentid="",
            originclass="")
    context = {
        'form': studentchangeclass
    }
    select_student_html=render_to_string("common/widget/select_student_change_class.html",context)
    return simplejson.dumps({"html":select_student_html})

@dajaxice_register
def saveChangeClass(request, form):
    form = studentchangeclassForm(deserialize_form(form))
    if form.is_valid():
        message = '转班成功'
        stuid = trip_str(form.cleaned_data["studentid"])
        student = StudentProfile.objects.get(baseinfo_studentid = stuid)
        student.small_class = SmallClass.objects.get(id = form.cleaned_data["receiveclass"])
        student.save()
    else:
        message = '转班失败'
    return simplejson.dumps({'message':message})

@dajaxice_register
def getStudentScore(request, studentid):
    selects = SelectCourse.objects.filter(student__baseinfo_studentid = studentid)
    for select in selects:
        select.score = Score.objects.get(select_obj = select)
    return render_to_string("widgets/student_score_table.html", {"selects": selects,})

@dajaxice_register
def getStudentList(request, year, page_numbers, cls, page):
    page = int(page)
    page_numbers = int(page_numbers)
    students = StudentProfile.objects.all()
    if year != "-1": students = students.filter(innovation_grade = year)
    if check_auth(request.user, TEACHER_USER):
        teacher = TeacherProfile.objects.get(userid = request.user)
        students = students.filter(small_class = teacher.small_class)
    elif cls != "-1":
        students = students.filter(small_class__practice_class__userid__username = cls)

    context = getContext(students, page, "item", 0, page_numbers)
    return render_to_string("teacher/widgets/student_set_table.html", context)

@dajaxice_register
def exportSearchStudents(request,searchform):
    searchform = StudentSearchForm(deserialize_form(searchform),request = request)
    stu_set = stuFilterList(request,searchform).order_by("small_class","innovation_grade")
    head_dict = {0:u'姓名',1:u'学号',2:u'所属班级',3:u'进入年份',4:u'性别',5:u'院系',6:u'邮箱',7:u'电话'}
    excelname = u"学生信息表"
    path = get_xls_path(request,head_dict,stu_set,excelname)
    return simplejson.dumps({'path':path})

#@dajaxice_register
#def SearchStudent(request):
#    identity = request.session.get('auth_role', "")
#    path = "common/widgets/student_search_table.html"
#    stu_set = StudentProfile.objects.all().order_by("small_class","innovation_grade")
#    context = {
#        "stu_set":stu_set,
#        "role":identity,
#    }
#    table = refresh_table(request,path,context)
#    return simplejson.dumps({'table':table,})

@dajaxice_register
def AddStudent(request,form):
    student_form = StudentAddForm(deserialize_form(form),request = request)
    if student_form.is_valid():
        name= trip_str(student_form.cleaned_data["baseinfo_name"])
        studentid= trip_str(student_form.cleaned_data["baseinfo_studentid"])
        smallclass = student_form.cleaned_data["small_class"]
        innovationgrade = trip_str(student_form.cleaned_data["innovation_grade"])
        if not isstudentExist(trip_str(studentid)):
            create_student(name,studentid,smallclass,innovationgrade)
            message = u'人员添加成功'
            status = '1'
        else:
            message = u'相同学号已存在'
            status = '0'
        ret = {'status':status,'message':message,}
    else:
        return simplejson.dumps({'status':"2",'message':u'输入有误，请重新输入','error_id': student_form.errors.keys(),})
    return  simplejson.dumps(ret)

def trip_str(strtmp):
    return strtmp.strip()

@dajaxice_register
def CoursePlanChange(request,courseplanform,iid,pid):
    if(iid==-1):
        form=CoursePlanForm(deserialize_form(courseplanform))
    else:
        form=CoursePlanForm(deserialize_form(courseplanform),instance=CoursePlan.objects.get(pk=iid))

    status=0
    courseplan_html=''
    if form.is_valid():
        if pid== -1:
            practice=PracticeProfile.objects.get(userid=request.user)
        else:
            practice=PracticeProfile.objects.get(pk=pid)
        courseplan=form.save(commit=False)
        courseplan.course_practice=practice
        courseplan.save()
        courseplan_html=render_to_string("widgets/course_plan_table.html",{
            "course_plan_list":practice.courseplan_set.all()
        })
    else:
        status=1
    return simplejson.dumps({
        'status':status,
        'error_list':form.as_p(),
        'courseplan_html':courseplan_html
    })


@dajaxice_register
def CoursePlanDelete(request,iid,pid):
    CoursePlan.objects.get(pk=iid).delete()
    if pid== -1:
        practice=PracticeProfile.objects.get(userid=request.user)
    else:
        practice=PracticeProfile.objects.get(pk=pid)
    courseplan_html=render_to_string("widgets/course_plan_table.html",{
        "course_plan_list":practice.courseplan_set.all()
    })
    return simplejson.dumps({
        'status':0,
        'courseplan_html':courseplan_html
    })
@dajaxice_register
def getSearchStudentPagination(request,page,searchform):
    message = ""
    role = request.session.get('auth_role',"")
    searchform = StudentSearchForm(deserialize_form(searchform),request = request)
    stu_set = stuFilterList(request,searchform).order_by("small_class","innovation_grade")
    context = getContext(stu_set,page,"item",0)
    context.update({"role":role})
    html = render_to_string("common/student/student_search_table.html",context)
    return simplejson.dumps({"message":message,"html":html})


@dajaxice_register
def GetCourseInfo(request,sid):
    if StudentProfile.objects.filter(baseinfo_studentid=sid).count() ==0:
        context={"message":u"没有该学号对应学生！"}
    else:
        student=StudentProfile.objects.get(pk=sid)
        context=selectCourseContext(request,student)
    select_table_html=render_to_string("widgets/select_course.html",context)
    ret = simplejson.dumps({"select_table_html":select_table_html})
    return ret



@dajaxice_register
def GetDeleteCourseInfo(request,sid):
    if StudentProfile.objects.filter(baseinfo_studentid=sid).count() ==0:
        context={"message":u"没有该学号对应学生！"}
    else:
        student=StudentProfile.objects.get(pk=sid)
        context=AdminDeleteCourseContext(student)
    delete_table_html=render_to_string("widgets/delete_course.html",context)
    return simplejson.dumps({"delete_table_html":delete_table_html})

@dajaxice_register
def StudentRegistration(requset,student_name,student_id,sex,tel_num):
    message=""
    try:
        user=User.objects.create_user(username=student_id,password=student_id)
        user.save()
        small_class=SmallClass.objects.filter(practice_class__nick_name="cxcy")[0]
        student=StudentProfile()
        student.baseinfo_name=student_name
        student.baseinfo_studentid=student_id
        student.baseinfo_sex=sex
        student.userid=user
        student.baseinfo_idcard="xx"
        student.contactinfo_telephone=tel_num
        student.small_class=small_class
        student.innovation_grade=2014
        student.save()
        status=0
    except Exception,e:
        print e
        message=u"学号已经存在或已参加实践班"
        status=1
    finally:
        return simplejson.dumps({"message":message,"status":status})
