#Create your views here.

from django.shortcuts import render
from common.models import Course
from backend.logging import loginfo
from common.utility import getWeek
from django.db.models import Q
from users.models import SmallClass,StudentProfile
from django.views.decorators import csrf
import datetime
@csrf.csrf_protect
def courseViews(request):
    now=datetime.datetime.now()
    if request.method=="POST":
        course_date=request.POST["course_day"] 
        now=datetime.datetime(year=int(course_date[:4]),month=int(course_date[5:7]),day=int(course_date[-2:]))
        
    week,dayth,school_year,school_term=getWeek(now)
    course_list=Course.objects.filter(course_id__course_term=school_term,start_year=school_year,class_week__category=week)
    query=[]
    for i in range(1,7):
        tt=dayth*10+i
        query.append(Q(class_time__category=tt))
    qq=reduce(lambda x,y:x|y,query)
    course_list=course_list.filter(qq).distinct()
    context={
        "course_list":course_list,
        "date":now
    }   
    return render(request,"president/course_of_today.html",context)

def practiceViews(request):
    classes=SmallClass.objects.all()
    now=datetime.datetime.now();
    if request.method=="POST":
        course_date=request.POST["course_day"] 
        now=datetime.datetime(year=int(course_date[:4]),month=int(course_date[5:7]),day=int(course_date[-2:]))
    dayth=now.isoweekday()
    cl=[]
    for item in classes:
        dic={
            "class_name":item.class_name
        }
        for d in range(1,7):
            kwargs = {}
            kwargs["small_class"] = item
            kwargs["practiceclasspractice__class_select_%d_%d" % (dayth, d)] = True
            students = StudentProfile.objects.filter(**kwargs)
            dic["time%d"%d]=students.count()
        cl.append(dic)

    context={
        "classes":cl,
        "date":now
    }
    return render(request,"president/practice_of_today.html",context)
