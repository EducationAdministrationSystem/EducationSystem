# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.views.decorators import csrf
from django.core.urlresolvers import reverse
from const import *
from users.models import ApplyInfo, PracticeProfile
from common.forms import  ApllyInfoForm

def getContext(request):
    if request.method == "POST":
        #student_id=request.POST.get('student_id',None)
        #if ApplyInfo.objects.filter(pk=student_id).count()> 0:
        #   student=ApplyInfo.objects.get(pk=student_id)
        #   form=ApllyInfoForm(request.POST,instance=student)
        #else:
        form = ApllyInfoForm(request.POST)
        stuId =  form.data['student_id']
        if ApplyInfo.objects.filter(student_id = stuId):
            ApplyInfo.objects.get(student_id = stuId).delete()
            print "delete"
        if form.is_valid():
            try:
                form.save()
            except:
                print "invalid"
            return "success"
    else:
        form = ApllyInfoForm()

    practice = PracticeProfile.objects.all()

    context = {
            "form":form,
            "practice": practice,
            "recruit":True
        }
    return context

@csrf.csrf_protect
def homeViews(request):
    context=getContext(request)
    if context=="success":
        return HttpResponseRedirect(reverse("recruit.views.responseViews"))
    return render(request, 'recruit/home.html', context)

def responseViews(request):
    return render(request, "recruit/response.html", {})


@csrf.csrf_protect
def homeMobileViews(request):
    context=getContext(request)
    if context=="success":
        return HttpResponseRedirect(reverse("recruit.views.responseMobileViews"))
    return render(request, 'recruit/home2.html', context)

def responseMobileViews(request):
    return render(request, "recruit/response2.html", {})

def registrationViews(request):
    return render(request,"recruit/registration.html",{})
