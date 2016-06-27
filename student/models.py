# coding=utf-8
from django.db import models
from users.models import TeacherProfile,StudentProfile,SmallClass
from common.utility import get_student_yearlist
from const import AGREE_CHOICE
#Create your models here.
class ChangeClassApply(models.Model):
    """docstring for ChangeClassApply"""
    YEAR_CHOICES = get_student_yearlist(type = "model")
    student = models.ForeignKey(StudentProfile,verbose_name=u"学生")
    originclass = models.ForeignKey(SmallClass,related_name='originclass',verbose_name=u"原实践班")
    originOK = models.IntegerField(null=False, default=1,choices=AGREE_CHOICE,verbose_name=u"原实践班意见")
    receiveclass = models.ForeignKey(SmallClass,related_name='receiveclass',verbose_name=u"接收实践班")
    receiveOK = models.IntegerField(null=False, default=1,choices=AGREE_CHOICE,verbose_name=u"接收实践班意见")
    deanOK = models.IntegerField(null=False, default=1,choices=AGREE_CHOICE,verbose_name=u"院长意见")
    innovation_grade = models.IntegerField(blank=False, choices=YEAR_CHOICES,null=False,
                               verbose_name=u"转入年份")
    class Meta:
        verbose_name = "学生转班"
        verbose_name_plural = "学生转班"
    def __unicode__(self):
        return '%s' % (self.student.baseinfo_name)

