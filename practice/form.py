#coding=utf-8
from django import forms
from users.models import SmallClass,StudentProfile,PracticeProfile

class ClassAddForm(forms.Form):
    nickname=forms.CharField(max_length=20,required=True,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"class_nickname"}))
    fullname=forms.CharField(max_length=30,required=True,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"class_fullname"}))

class SmallClassAddForm(forms.Form):
    

    class_name=forms.CharField(max_length=30,required=True,
                            widget=forms.TextInput(attrs={'class':'form-control','id':"class_name"}))
    practice_class=forms.ChoiceField(required=True,choices = [],label=u"实践班",
                                   widget=forms.Select(attrs={'class':'form-control','id':"practice_class"}),)
    def __init__(self, *args, **kwargs):
        super(SmallClassAddForm, self).__init__(*args, **kwargs)
        practice_list = PracticeProfile.objects.all()
        PRACTICE_CHOICES_list=[]
        for obj in practice_list:
            PRACTICE_CHOICES_list.append((obj.id,obj.full_name))
        self.fields["practice_class"].choices=tuple(PRACTICE_CHOICES_list)

class ClassChaneForm(forms.Form):
    SMALL_CHOICES_list = [(-1, u"所有小班")]
    small_list = SmallClass.objects.all()
    for obj in small_list:
        SMALL_CHOICES_list.append((obj.id, obj.class_name))
    SMALL_CHOICES = tuple(SMALL_CHOICES_list)
    YEAR_CHOICES_list = [(-1, u"年份")]
    year_list = StudentProfile.objects.values('innovation_grade').distinct()
    for tmp in year_list:
        for  key in tmp:
            YEAR_CHOICES_list.append((str(tmp[key]),str(tmp[key])))
    YEAR_CHOICES = tuple(YEAR_CHOICES_list)
    origin_small_class = forms.ChoiceField(
                                   required=True,choices = SMALL_CHOICES,label=u"原实践班",
                                   widget=forms.Select(attrs={'class':'form-control','id':"origin_small_class"}),)
    recieve_small_class = forms.ChoiceField(
                                   required=True,choices = SMALL_CHOICES,label=u"接收实践班",
                                   widget=forms.Select(attrs={'class':'form-control','id':"recieve_small_class"}),)
    innovation_grade = forms.ChoiceField(
                                   required=True,choices = YEAR_CHOICES,label=u"转入年份",
                                   widget=forms.Select(attrs={'class':'form-control','id':"innovation_grade"}),)