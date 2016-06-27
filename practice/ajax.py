#cmcoding: utf-8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template.loader import render_to_string
from django.db.models import Q
from common.models import Course,SelectCourse
from backend.utility import getContext
from users.models import ApplyInfo, PracticeProfile, StudentProfile
import datetime
from common.forms import SmallClassForm
from common.utility import create_student, isstudentExist
from adminStaff.utility import get_xls_path

@dajaxice_register
def studentEntry(request, apply_list, small_class_id):
    for student_id in apply_list:
        apply = ApplyInfo.objects.get(student_id = student_id)
        if not isstudentExist(student_id): 
            create_student(apply.student_name, apply.student_id, small_class_id, apply.innovation_grade, apply.sex, apply.tel_num, apply.email, apply.apartment, apply.college)       
    return simplejson.dumps({})

@dajaxice_register
def getApplys(request, page):
    page = int(page)
    applys = ApplyInfo.objects.filter(innovation_grade = datetime.datetime.today().year)
    practice = PracticeProfile.objects.get(userid = request.user)
    applys = applys.filter(Q(wish_first = practice.id) | Q(wish_second = practice.id))

    for apply in applys:
        apply.is_first_wish = "是" if apply.wish_first == practice else "否"
        try:
            apply.small_class = "已录入(%s)" % StudentProfile.objects.get(baseinfo_studentid = apply.student_id).small_class
        except:
            apply.small_class = "未录入"
    number, first_number = applys.count(), applys.filter(wish_first = practice.id).count()
    applys = sorted(list(applys), key=lambda x: x.is_first_wish, reverse = True)
    context = getContext(applys, page, "item", 0)

    context.update({"number": number, 
                    "first_number": first_number,
                    "practice": practice, })

    return render_to_string("practice/widgets/applys.html", context)

@dajaxice_register
def exportEntryList(request):
    practice = PracticeProfile.objects.get(userid = request.user)
    applys = ApplyInfo.objects.filter(innovation_grade = datetime.datetime.today().year)
    practice = PracticeProfile.objects.get(userid = request.user)
    applys = applys.filter(Q(wish_first = practice.id) | Q(wish_second = practice.id))
    for apply in applys:
        apply.is_first_wish = u"是" if apply.wish_first == practice else u"否"
    applys = sorted(list(applys), key=lambda x: x.is_first_wish, reverse = True)
    head_list = {0: "姓名", 1: "性别", 2: "学号", 3: "电话", 4: "邮箱", 5: "学部",
                 6: "学院", 7: "是否为第一志愿", }
    excelname = practice.full_name + u"招新信息汇总"
    return get_xls_path(request, head_list, applys, excelname)

@dajaxice_register
def getComment(request,courseid):
    course = Course.objects.get(id=courseid)
    evalutionlist = [obj.evalution for obj in SelectCourse.objects.filter(course=course)]
    # evalutionlist = SelectCourse.objects.filter(course=course)
    context ={
        'evalutionlist':evalutionlist,
    }
    form_html = render_to_string("practice/widgets/comment_table.html",context)
    return simplejson.dumps({"form_html":form_html})
