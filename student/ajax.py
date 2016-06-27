from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from django.template.loader import render_to_string
from common.models import Course,SelectCourse
from backend.utility import getContext
from users.models import ApplyInfo, PracticeProfile, StudentProfile
from student.models import ChangeClassApply

@dajaxice_register
def getComment(request,courseid):
    stu = StudentProfile.objects.get(userid = request.user)
    #course = SelectCourse.objects.filter(student = stu)
    comment = SelectCourse.objects.filter(id = courseid,student = stu)
    # evalutionlist = SelectCourse.objects.filter(course=course)
    context ={
        'comment':comment,
    }
    form_html = render_to_string("student/widgets/comment.html",context)
    return simplejson.dumps({"form_html":form_html})

@dajaxice_register
def classChangeDelete(request,student):
	classChange = ChangeClassApply.objects.filter(student = student)
	classChange.delete()