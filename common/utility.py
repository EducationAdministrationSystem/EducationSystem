# coding=utf-8
from django.contrib.auth.models import User
from django.db.models import Q
from users.models import StudentProfile,SmallClass,TeacherProfile
from django.template.loader import render_to_string
from users.models import StudentProfile,SmallClass,PracticeProfile
from const.models import AdminSetting
from common.models import Course, PracticeClassPractice,SelectCourse, Score, Homework, HomeworkSubmit, CoursePlan,SmallClassPractice
import datetime
from const import GRADE_IGNORE,STUDENT_USER
from const.models import ClassRoom

def create_student(name,studentid,smallclassid,innovationgrade, sex=None, tel_num=None, email=None, apartment=None, college=None):
        user = User.objects.create_user(username = studentid,password = studentid)
        smallclass = SmallClass.objects.get(id =  smallclassid)
        user.save()
        try:
            newstu = StudentProfile()
            newstu.userid = user
            newstu.baseinfo_name = name
            newstu.baseinfo_studentid = studentid
            newstu.small_class = smallclass

            newstu.baseinfo_sex = sex
            newstu.contactinfo_telephone=tel_num
            newstu.contactinfo_email = email
            newstu.collegeinfo_apartment = apartment
            newstu.collegeinfo_college = college

            if innovationgrade != "-1":
                newstu.innovation_grade = innovationgrade
            newstu.save()
        except Exception, e:
            raise e

def isstudentExist(studentid):
    studentset = StudentProfile.objects.filter(baseinfo_studentid = studentid)
    userset = User.objects.filter(username = studentid)
    if studentset or userset:
        return True
    else:
        return False

def isClassExisted(full_name,nick_name):
    classset = PracticeProfile.objects.filter(nick_name=nick_name)
    if classset:
        return True
    else:
        return False

def isSmallClassExisted(fullname,practice_class):
    classset = SmallClass.objects.filter(class_name=fullname)
    if classset:
        return True
    else:
        return False

def isteacherExist(teacherid):
    teacherset = TeacherProfile.objects.filter(teacher_id = teacherid)
    if teacherset:
        return True
    else:
        return False

def delete_teacher(teacherid):
    TeacherProfile.objects.get(teacher_id=teacherid).userid.delete()

def create_teacher(name,teacherid,smallclassid):
    user = User.objects.create_user(username = teacherid,password = teacherid)
    smallclass = SmallClass.objects.get(id = smallclassid)
    user.save()
    newteacher = TeacherProfile()
    newteacher.userid = user
    newteacher.teacher_name = name
    newteacher.teacher_id = teacherid
    newteacher.small_class = smallclass
    newteacher.save()

def create_class(full_name,nick_name):
    user =User.objects.create_user(username = nick_name,password='1')
    user.save()
    cla = PracticeProfile()
    cla.userid=user
    cla.full_name=full_name
    cla.nick_name=nick_name
    cla.save()

def create_smallclass(class_name,practice_class):
    cla = SmallClass()
    cla.class_name=class_name
    cla.practice_class=PracticeProfile.objects.get(pk=practice_class)
    cla.save()
    cla.brother_class=cla
    cla.save()
    for i in range(1, 4):
        nscp = SmallClassPractice(small_class = cla, class_grade = i)
        nscp.save()

def get_student_yearlist(type=None):
    year_list = StudentProfile.objects.values('innovation_grade').distinct().order_by('innovation_grade')
    YEAR_CHOICES_list = []
    if type != "model":
        YEAR_CHOICES_list.append((-1, u"年份"))
    for tmp in year_list:
        for  key in tmp:
            YEAR_CHOICES_list.append((tmp[key],tmp[key]))
    YEAR_CHOICES = tuple(YEAR_CHOICES_list)
    return YEAR_CHOICES
def get_small_classlist(request):
    identity = request.session.get('auth_role', "")
    if identity == "practice":
        practiceclass = PracticeProfile.objects.get(userid = request.user)
        small_list = SmallClass.objects.filter(practice_class = practiceclass)
    elif identity == "teacher":
        teacher = TeacherProfile.objects.get(userid = request.user)
        small_list = SmallClass.objects.filter(id = teacher.small_class.id)
    else:
        small_list = SmallClass.objects.all()
    if identity == "teacher":
        SMALL_CHOICES_list = []
    else:
        SMALL_CHOICES_list = [(-1, u"所有小班")]
    for obj in small_list:
        SMALL_CHOICES_list.append((obj.id, obj.class_name))
    SMALL_CHOICES = tuple(SMALL_CHOICES_list)
    return SMALL_CHOICES

def get_practice_classlist(request):
    identity = request.session.get('auth_role', "")
    if identity == "practice":
        practice_list = PracticeProfile.objects.filter(userid = request.user)
    elif identity == "teacher":
        teacher = TeacherProfile.objects.get(userid = request.user)
        practice_list = PracticeProfile.objects.filter(id = teacher.small_class.practice_class.id)
    else:
        practice_list = PracticeProfile.objects.all()
    if identity == "adminStaff":
        PRACTICE_CHOICES_list = [(-1, u"所有大班")]
    else:
        PRACTICE_CHOICES_list = []
    for obj in practice_list:
        PRACTICE_CHOICES_list.append((obj.id, obj.full_name))
    PRACTICE_CHOICES = tuple(PRACTICE_CHOICES_list)
    return PRACTICE_CHOICES

def refresh_table(request,path,context):
    """
        reload partial html
        @path:the html location
        @context
    """
    return render_to_string(path,context)
def getStudentGrade(student):
    admin_setting=AdminSetting.objects.all()[0]
    school_year=admin_setting.school_year.school_year
    year=int(school_year[-4:])
    grade=year-student.innovation_grade
    return grade
def getYearbyGrade(grade):
    grade=int(grade)
    admin_setting=AdminSetting.objects.all()[0]
    school_year=admin_setting.school_year.school_year
    year=int(school_year[-4:])
    return year-grade


def selectCourseContext(request,student):
    # student = StudentProfile.objects.get(userid = request.user)
    grade = getStudentGrade(student)
    now=datetime.datetime.now()
    admin_setting=AdminSetting.objects.all()[0]
    select_start=admin_setting.course_select_start
    select_end=admin_setting.course_select_end
    school_year=admin_setting.school_year
    year=int(school_year.school_year[-4:])
    switch=admin_setting.course_select_switch
    identity=request.session.get('auth_role',"")
    message=""
    if identity==STUDENT_USER and switch==False and (select_start==None or now<select_start or now>select_end):
        message=u"非选课阶段不能选课！"
    if student.baseinfo_idcard == None:
        message=u"完善个人信息之后才能进行选课！"
    grade=year-student.innovation_grade

    print "$$$$$:" ,admin_setting.school_term
    # course_list=Course.objects.filter(course_to_class=student.small_class,course_id__course_term=admin_setting.school_term,start_year=school_year)
    course_list=Course.objects.filter(Q(course_to_class=student.small_class)
                                      & Q(start_year=school_year)
                                      & (Q(course_id__course_grade = grade)
                                      | Q(course_id__course_grade = -1)))
    course_list = course_list.filter(Q(course_id__course_term=admin_setting.school_term)|Q(course_id__course_term=-1))
    # course_list=course_list.filter(Q(course_id__course_grade=grade)|Q(course_id__course_grade=-1))
    course_list=course_list.filter(Q(course_id__course_grade__lte=grade)|Q(course_id__course_plan_id__in=GRADE_IGNORE))
    if course_list.count()==0 and message == "":
        message=u"没有可选择课程！"

    for item in course_list:
        item.remaining= item.class_capacity-item.int_nelepeo
        if SelectCourse.objects.filter(student=student,course=item).count()>0:
            item.selected=1
        else:
            item.selected=0
    context={
        "message":message
    }
    if message =="":
        context.update({
            "course_list":course_list
        })
    return context

def DeleteCourseContext(student):
    selected_course=[]
    admin_setting=AdminSetting.objects.all()[0]
    school_year=admin_setting.school_year
    term=admin_setting.school_term
    for item in student.selectcourse_set.filter(course__start_year=school_year,course__course_id__course_term=term):
        course=item.course
        selected_course.append(course)
    message =""
    if len(selected_course)== 0:
        message ==u"没有选择任何课程！"

    context={
        "message":message,
        "course_list":selected_course,
    }
    return context

def AdminDeleteCourseContext(student):
    selected_course=[]
    admin_setting=AdminSetting.objects.all()[0]
    for item in student.selectcourse_set.all():
        course=item.course
        selected_course.append(course)
    message =""
    if len(selected_course)== 0:
        message ==u"没有选择任何课程！"

    context={
        "message":message,
        "course_list":selected_course,
    }
    return context

def getHomeworkScore(student, course):
    homework_set = HomeworkSubmit.objects.filter(Q(student = student) & Q(homework__course = course))
    if homework_set.count():
        return sum(homework.score for homework in homework_set if homework.score) / homework_set.count()
    return 0


def getWeek(now):
    now.replace(hour=0,minute=0,second=0)
    admin_setting=AdminSetting.objects.all()[0]
    firstday=admin_setting.tearm_first_day
    days=(now-firstday).days
    print now,firstday,days
    week = days/7+1
    dayth=days%7+1
    return (week,dayth,admin_setting.school_year,admin_setting.school_term)

def isClassRoomExist(name):
    classRoomSet=ClassRoom.objects.filter(room_name = name)
    if classRoomSet:
        return True
    else:
        return False

def create_classroom(name):
    classroom = ClassRoom()
    classroom.room_name = name
    classroom.save()
