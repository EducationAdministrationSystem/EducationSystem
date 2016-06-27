# coding=utf-8
from django import forms
from const import *
from const.models import SchoolYear
from users.models import StudentProfile, PracticeProfile, ApplyInfo
from common.models import CoursePlan
from users.models import StudentProfile, PracticeProfile, ApplyInfo, SmallClass, getPractices

class SmallClassForm(forms.Form):
    small_classes = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control', "style": "width: 200px"}))
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super(SmallClassForm, self).__init__(*args, **kwargs)
        SMALL_CLASS_CHOICES = tuple((small_class.id, small_class) for small_class in SmallClass.objects.filter(practice_class__userid = request.user))
        self.fields["small_classes"].choices = SMALL_CLASS_CHOICES

class CourseFilterForm(forms.Form):
    classes = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control course_filter'}))
    terms = forms.ChoiceField(choices = TERM_CHOICE, widget = forms.Select(attrs={'class': 'form-control course_filter'}))
    grades = forms.ChoiceField(choices = GRADE_CHOICE, widget = forms.Select(attrs={'class': 'form-control course_filter'}))
    years = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control course_filter'}))
    page_numbers = forms.ChoiceField(choices = PAGE_CHOICE, required=False,widget = forms.Select(attrs={'class': 'form-control course_filter'}))
    def __init__(self, *args, **kwargs):
        super(CourseFilterForm, self).__init__(*args, **kwargs)
        YEAR_CHOICES = ((-1, u"全部"), ) + tuple((year.id, year) for year in SchoolYear.objects.all())
        self.fields["years"].choices = YEAR_CHOICES

        CLASS_CHOICES = ((-1, u"全部"), ) + tuple((practice.userid, practice) for practice in PracticeProfile.objects.all())
        self.fields["classes"].choices = CLASS_CHOICES


class StudentFilterForm(forms.Form):
    classes = forms.ChoiceField(choices = CLASS_CHOICES, widget = forms.Select(attrs={'class': 'form-control student_filter'}))
    years = forms.ChoiceField(widget = forms.Select(attrs={'class': 'form-control student_filter'}))
    page_numbers = forms.ChoiceField(choices = PAGE_CHOICE, widget = forms.Select(attrs={'class': 'form-control student_filter'}))
    def __init__(self, *args, **kwargs):
        super(StudentFilterForm, self).__init__(*args, **kwargs)
        YEAR_CHOICES = sorted(tuple(set((student.innovation_grade, student.innovation_grade) for student in StudentProfile.objects.all())), reverse = True)
        YEAR_CHOICES = ((-1, u"全部"), ) + tuple(YEAR_CHOICES)
        self.fields["years"].choices = YEAR_CHOICES

        CLASS_CHOICES = ((-1, u"全部"), ) + tuple((practice.userid, practice) for practice in PracticeProfile.objects.all())
        self.fields["classes"].choices = CLASS_CHOICES

class ApllyInfoForm(forms.ModelForm):
    def clean_wish_second(self):
        first = self.cleaned_data.get("wish_first")
        second = self.cleaned_data.get("wish_second")
        if first == second:
            raise forms.ValidationError("两个志愿不能相同")
        return second
    class Meta:
        model=ApplyInfo
        exclude=("innovation_grade",)   
        widgets={
            'student_name':forms.TextInput(attrs={'class':'form-control regis-input','placeholder':u"姓名"}),
            'sex':forms.Select(attrs={'class':'form-control regis-input', 'placeholder':u'性别'}),
            'student_id':forms.TextInput(attrs={"class":'form-control regis-input', 'placeholder': '学号'}),
            'tel_num':forms.TextInput(attrs={"class":'form-control regis-input', 'placeholder': '电话'}),
            'email':forms.TextInput(attrs={"class":'form-control regis-input', 'placeholder': '邮箱'}),
            'apartment':forms.Select(attrs={'class':'form-control regis-input', }),
            'college':forms.Select(attrs={'class':'form-control regis-input'}),
			'wish_first':forms.Select(attrs={'class':'form-control regis-input'}),
            'wish_second':forms.Select(attrs={'class':'form-control regis-input'}),
            'self_introduction':forms.Textarea(attrs={'class':'form-control','placeholder':u"请做简单自我介绍，包括自己特长和参加科技竞赛获奖经历(300字以内)。"})
        }


class CoursePlanForm(forms.ModelForm):
    class Meta:
        model=CoursePlan
        exclude=('course_practice')
        widgets={
            'course_plan_id':forms.TextInput(attrs={"class":'form-control','style':'width:50%'}),
            'course_name':forms.TextInput(attrs={"class":'form-control','style':'width:50%'}),
            'course_grade':forms.Select(attrs={"class":'form-control','style':'width:50%'}),
            'course_term':forms.Select(attrs={"class":'form-control','style':'width:50%'}),
            'course_point':forms.TextInput(attrs={"class":'form-control','style':'width:50%'}),
        }


