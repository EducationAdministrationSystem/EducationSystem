# coding: UTF-8
from django import  forms
from backend.logging import loginfo
from common.models import Course, SmallClassPractice
from users.models import TeacherProfile,PracticeProfile, SmallClass
from const.models import ClassRoom
from common.utility import get_student_yearlist

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields={'course_id','teacher','class_place','course_to_class','practice_periods','theory_periods','class_capacity','start_year','class_week','class_time'}
        widgets = {'course_id':forms.Select(attrs={"class":'form-control'}),
                   'teacher':forms.Select(attrs={"class":'form-control'}),
                   'class_week':forms.SelectMultiple(attrs={"class":'form-control'}),
                   'class_time':forms.SelectMultiple(attrs={"class":'form-control'}),
                   'class_place':forms.Select(attrs={"class":'form-control'}),
                   'course_to_class':forms.SelectMultiple(attrs={"class":'form-control' }),
                   'practice_periods':forms.TextInput(attrs={"class":'form-control'}),
                   'theory_periods':forms.TextInput(attrs={"class":'form-control'}),
                   'class_capacity':forms.TextInput(attrs={"class":'form-control'}),
                   'start_year':forms.Select(attrs={"class":'form-control'}),
                  }
    def __init__(self,*args,**kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields["class_place"].choices = [(obj.id,obj.room_name) for obj in ClassRoom.objects.all()]

class SmallClassSelectForm(forms.Form):
    smallClass = forms.ChoiceField(choices=[], required=False,
                                   widget = forms.Select(attrs = {
                                       'class': 'form-control',
                                       'style': 'width: 200px',
                                       'id': 'smallClassSelect',
                                       'autocomplete': "off",
                                   }), label = u"选择实践小班")
    def __init__(self, *args, **kwargs):
        super(SmallClassSelectForm, self).__init__(*args, **kwargs)
        #allSmallClass = SmallClass.objects.all()
        #for sc in allSmallClass:
            #for i in range(1, 4):
                #nscp = SmallClassPractice(small_class = sc, class_grade = i)
                #nscp.save()
        
        allSmallClass = SmallClassPractice.objects.all()
        choiceList = [('-1', '----')]
        for sc in allSmallClass:
            choiceList.append((sc.id, sc.__unicode__()))
        self.fields["smallClass"].choices = tuple(choiceList)
class PracticeSelectForm(forms.Form):
    practice = forms.ChoiceField(choices=[], required=False,
                                   widget = forms.Select(attrs = {
                                       'class': 'form-control',
                                       'style': 'width: 200px',
                                       'id': 'PracticeSelect',
                                       'autocomplete': "off",
                                   }), label = u"选择实践班")
    def __init__(self, *args, **kwargs):
        super(PracticeSelectForm, self).__init__(*args, **kwargs)
        allPractice = PracticeProfile.objects.all()
        choiceList = [('-1', '----')]
        for sc in allPractice:
            choiceList.append((sc.id, sc.full_name))
        self.fields["practice"].choices = tuple(choiceList)

class ClassRoomForm(forms.Form):
    room_name=forms.ChoiceField(choices=[],required=False,
                                widget=forms.Select(attrs={
                                    'class':'form-control',
                                    'style':'width:200px',
                                    'id':'ClassRoom',
                                }),label=u"选择教室")
    def __init__(self,*args,**kwargs):
        super(ClassRoomForm,self).__init__(*args,**kwargs)
        allRoom=ClassRoom.objects.all()
        choiceList=[('-1','----')]
        for r in allRoom:
            choiceList.append((r.id,r.room_name))
        self.fields["room_name"].choices=tuple(choiceList)

class classRoomAddForm(forms.ModelForm):
  class Meta:
    model = ClassRoom
    widgets ={
      'room_name':forms.TextInput(attrs={"class":'form-control'}),
    }

class ImportDataForm(forms.Form):
    document = forms.FileField(label='select', help_text='文件上传', required=False)

class GradeYearForm(forms.Form):
    grade_year=forms.ChoiceField(choices=[],required=False,
                                widget = forms.Select(attrs = {
                                       'class': 'form-control',
                                       'style': 'width: 200px',
                                       'id': 'GradeYearSelect',
                                   }), label = u"选择入学年份")
    def __init__(self,*args,**kwargs):
        super(GradeYearForm,self).__init__(*args,**kwargs)
        YEAR_CHOICES = get_student_yearlist()
        self.fields["grade_year"].choices=YEAR_CHOICES
