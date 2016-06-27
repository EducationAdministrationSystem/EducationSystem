#!/usr/bin/env python
# coding=utf-8


from django import forms
from django.forms import ModelForm
from common.models import Homework, HomeworkSubmit, SmallClassPractice
from users.models import SmallClass
from common.models import Course
from const import GRADE_CHOICE

class RatioSetForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('attendance_rate', 'homework_rate', 'final_rate')
        widgets = {
            "attendance_rate": forms.TextInput(attrs={"class": "form-control", "style": "width: 80px"}),
            "homework_rate": forms.TextInput(attrs={"class": "form-control", "style": "width: 80px"}),
            "final_rate": forms.TextInput(attrs={"class": "form-control", "style": "width: 80px"}),
        }
class HomeworkForm(ModelForm):
    class Meta:
        model = Homework
        fields = ('name', 'required', 'deadline', 'is_final')
        widgets = {

            'name': forms.TextInput(attrs={'class':'form-control','style':'width:170px',}),
            'required': forms.Textarea(attrs={'class':'form-control', 'row':10,}),
            'deadline': forms.DateTimeInput(attrs={'class':'form-control', 'style':'width:170px',}),
            'is_final':forms.CheckboxInput(attrs={'id':'homework_is_final',}),

        }



class SmallClassForm(forms.ModelForm):
    class Meta:
        model = SmallClassPractice
        exclude = ('small_class','class_grade')
        widgets = {
            "class_remain_1_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_1_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_1_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_1_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_1_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_1_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_2_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_3_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_4_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_5_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_6_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_1":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_2":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_3":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_4":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_5":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
            "class_remain_7_6":forms.TextInput(attrs={'class':"form-control",'style':"width:80px"}),
        }

class TeacherAddForm(forms.Form):
    baseinfo_teacherid = forms.CharField(max_length=20,required=True,
                                        widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_teacherid"}),)
    baseinfo_name = forms.CharField(max_length=20,required=True,
                                    widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_name"}),)
    small_class = forms.ChoiceField(required = True,choices = [],
                                    widget=forms.Select(attrs={'class':'form-control','id':"small_class"}),)
    teacher_email = forms.EmailField(required=False,max_length=100,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"teacher_email"}))
    teacher_telephone = forms.CharField(required=False,max_length=20,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"teacher_telephone"}))
    office_address=forms.CharField(required=False,max_length=50,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"office_address"}))
    office_phone=forms.CharField(required=False,max_length=30,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"office_phone"}))
    def __init__(self, *args, **kwargs):
        super(TeacherAddForm, self).__init__(*args, **kwargs)
        small_list = SmallClass.objects.all()
        choiceList = []
        for sc in small_list:
            choiceList.append((sc.id, sc.class_name))
        self.fields["small_class"].choices = tuple(choiceList)


class TeacherSearchForm(forms.Form):
    SMALL_CHOICES_list = [("","")]
    small_list = SmallClass.objects.all()
    for obj in small_list:
        SMALL_CHOICES_list.append((obj.id, obj.class_name))
    SMALL_CHOICES = tuple(SMALL_CHOICES_list)
    baseinfo_teacherid = forms.CharField(max_length=20,required=False,
                                        widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_teacherid"}),)
    baseinfo_name = forms.CharField(max_length=20,required=False,
                                    widget=forms.TextInput(attrs={'class':'form-control','id':"baseinfo_name"}),)
    small_class = forms.ChoiceField(required = False,choices = SMALL_CHOICES,
                                    widget=forms.Select(attrs={'class':'form-control','id':"small_class"}),)


class GradeForm(forms.Form):
    grade_choices = [('-1', '----')]
    for it in GRADE_CHOICE:
        grade_choices.append(it)
    grade_choice = forms.ChoiceField(required = True, choices = tuple(grade_choices),
                                    widget=forms.Select(attrs={
                                        'class':'form-control',
                                        'id':"gradeSelect",
                                        'style': 'width: 200px',
                                        'autocomplete': "off",}),)
