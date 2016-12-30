#!/usr/bin/env python
# coding=utf-8

from django import forms
from users.models import StudentProfile,StudentProfile,SmallClass,PracticeProfile
import types
from users.models import StudentProfile,StudentProfile,SmallClass
from common.models import PracticeClassPractice
from student.models import ChangeClassApply
from common.utility import get_student_yearlist,get_small_classlist,get_practice_classlist
from const import AGREE_CHOICE
from backend.logging import loginfo
class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ('userid','baseinfo_name','baseinfo_studentid','innovation_grade','innovation_class','small_class',)
        widgets = {
          "baseinfo_birth":forms.DateInput(attrs={'class':"form-control",}),
          "baseinfo_sex":forms.Select(attrs={'class':"form-control"}),
          "baseinfo_nation":forms.TextInput(attrs={'class':"form-control"}),
          "baseinfo_idcard":forms.TextInput(attrs={'class':"form-control"}),
          "collegeinfo_apartment":forms.Select(attrs={'class':"form-control"}),
          "collegeinfo_college":forms.Select(attrs={'class':"form-control"}),
          "collegeinfo_major":forms.TextInput(attrs={'class':"form-control"}),
          "collegeinfo_class":forms.TextInput(attrs={'class':"form-control"}),
          "contactinfo_dormitory":forms.TextInput(attrs={'class':"form-control"}),
          "contactinfo_telephone":forms.TextInput(attrs={'class':"form-control"}),
          "contactinfo_email":forms.TextInput(attrs={'class':"form-control"}),
                  }

class StudentAddForm(forms.Form):
    YEAR_CHOICES = get_student_yearlist()
    baseinfo_studentid = forms.CharField(max_length=20,label=u"学号",
                                 required=True,
                                 widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_studentid","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),)
    baseinfo_name = forms.CharField(max_length=100,label=u"姓名",
                                   required=True,
                                   widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_name",}),)
    small_class = forms.ChoiceField(
                                   required=True,label=u"班级",
                                   widget=forms.Select(attrs={'class':'form-control','id':"small_class",'label':u"班级",}),)
    innovation_grade = forms.ChoiceField(
                                   required=False,label=u"年份",choices = YEAR_CHOICES,
                                   widget=forms.Select(attrs={'class':'form-control','id':"innovation_grade",'placeholder':u"默认当前年份"}),)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(StudentAddForm, self).__init__(*args, **kwargs)
        if not request:
            return
        SMALL_CHOICES = get_small_classlist(request)
        self.fields["small_class"].choices = SMALL_CHOICES
    def clean_small_class(self):
        data = self.cleaned_data['small_class']
        if data == "-1":
            raise forms.ValidationError("small_class is not valid")
        return data


class StudentSearchForm(forms.Form):
    YEAR_CHOICES = get_student_yearlist()

    practice_class = forms.ChoiceField(
                                   required=True,label=u"大班",
                                   widget=forms.Select(attrs={'class':'form-control','id':"practice_class",}),)
    small_class = forms.ChoiceField(
                                   required=True,label=u"小班",
                                   widget=forms.Select(attrs={'class':'form-control','id':"small_class",}),)
    innovation_grade = forms.ChoiceField(
                                   required=False,choices = YEAR_CHOICES,label="进入年份",
                                   widget=forms.Select(attrs={'class':'form-control','id':"innovation_grade",}),)
    baseinfo_name_studentid = forms.CharField(max_length=100,label=u"模糊查询",
                                   required=False,
                                   widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_name_studentid",'placeholder':u"姓名或学号"}),)
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(StudentSearchForm, self).__init__(*args, **kwargs)
        if not request:
            return
        SMALL_CHOICES = get_small_classlist(request)
        PRACTICE_CHOICES = get_practice_classlist(request)
        self.fields["small_class"].choices = SMALL_CHOICES
        self.fields["practice_class"].choices = PRACTICE_CHOICES

class ClassChangeForm(forms.ModelForm):
    class Meta:
        model = ChangeClassApply
        fields = ("receiveclass","innovation_grade",)
        widgets = {
            "receiveclass" : forms.Select(attrs={'class':'form-control','id':"innovation_grade"}),
            "innovation_grade" : forms.Select(attrs={'class':'form-control','id':"innovation_grade"}),
        }
    def save(self, student,originclass ,commit=True):
        classchange = super(ClassChangeForm, self).save(commit=False)
        classchange.student = student
        classchange.originclass = originclass
        if commit:
            classchange.save()
        return classchange

class SelectSmallClassForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        context = kwargs.get("context", None)
        if context:
            del kwargs["context"]
        super(SelectSmallClassForm, self).__init__(*args, **kwargs)
        if context:
            for i in range(1, 8):
                for j in range(1, 7):
                    fieldName = "class_remain_%d_%d" % (i, j)
                    if context[fieldName] <= 0:
                        self.fields["class_select_%d_%d" % (i, j)].widget.attrs["disabled"] = "true"
    def update(self, *args, **kwargs):
        context = kwargs.get("context", None)
        if context:
            for i in range(1, 8):
                for j in range(1, 7):
                    fieldName = "class_remain_%d_%d" % (i, j)
                    if context[fieldName] <= 0:
                        self.fields["class_select_%d_%d" % (i, j)].widget.attrs["disabled"] = "true"
    class Meta:
        model = PracticeClassPractice
        exclude = ('student', )
        widgets = {
            "class_select_1_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_1_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_1_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_1_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_1_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_1_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_2_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_3_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_4_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_5_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_6_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_1":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_2":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_3":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_4":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_5":forms.CheckboxInput(attrs={'style':"width:30px"}),
            "class_select_7_6":forms.CheckboxInput(attrs={'style':"width:30px"}),
        }

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=100,widget=forms.Textarea(attrs={'style':"width:550px;height:150px"}))
    courseid = forms.CharField(max_length=100)
class ClassChangePreviewForm(forms.Form):
    classchange_agree_choice = list(AGREE_CHOICE)
    classchange_agree_choice = tuple( classchange_agree_choice)

    classchange_agree = forms.ChoiceField(choices=classchange_agree_choice,
      widget=forms.Select(attrs={'class':'form-control','style':"width:300px;"}),)

class studentchangeclassForm(forms.Form):
    studentname = forms.CharField(max_length=100,label=u"姓名",widget=forms.forms.TextInput(attrs={'class':'form-control col-lg-3','style':'readonly:readonly!important'}))
    studentid = forms.CharField(max_length=100,label=u"学号",widget=forms.forms.TextInput(attrs={'class':'form-control col-lg-3','style':'readonly:readonly!important'}))
    originclass = forms.CharField(max_length=100,label=u"原实践班",widget=forms.forms.TextInput(attrs={'class':'form-control col-lg-3','style':'readonly:readonly!important'}))
    receiveclass = forms.ChoiceField(choices=[],label=u"转入实践班",
      widget=forms.Select(attrs={'class':'form-control col-lg-3'}),)
    def __init__(self, *args, **kwargs):

        flag = False
        if kwargs.has_key('studentname'):
            flag = True
            studentname = kwargs['studentname']
            studentid = kwargs['studentid']
            originclass = kwargs['originclass']

            del kwargs['studentname']
            del kwargs['studentid']
            del kwargs['originclass']

        super(studentchangeclassForm, self).__init__(*args, **kwargs)

        if flag:
            self.fields['studentname'].initial = studentname
            self.fields['studentid'].initial = studentid
            self.fields['originclass'].initial = originclass

        allPractice = SmallClass.objects.all()
        choiceList = [('-1', '----')]
        for sc in allPractice:
            choiceList.append((sc.id, sc.class_name))
        self.fields["receiveclass"].choices = tuple(choiceList)
