# coding: UTF-8
from django.db import models
from django.contrib.auth.models import User
from const import *

class SchoolYear(models.Model):
    school_year=models.CharField(blank=False,max_length=20,unique=True,verbose_name=u"学年")
    class Meta:
        verbose_name = "学年"
        verbose_name_plural = "学年"
    def __unicode__(self):
        return '%s'% self.school_year

class ClassTime(models.Model):
    category = models.IntegerField(blank=False, unique=True,
                                choices=CLASSTIME_CHOICES,
                                verbose_name=u"上课时间")
    class Meta:
        verbose_name = "上课时间表"
        verbose_name_plural = "上课时间表"
    def __unicode__(self):
        return self.get_category_display()
class WeekTime(models.Model):
    category = models.IntegerField(blank=False, unique=True,
                                choices=WEEKTIME_CHOICES,
                                verbose_name=u"上课周次")
    class Meta:
        verbose_name = "上课周次表"
        verbose_name_plural = "上课周次表"
    def __unicode__(self):
        return self.get_category_display()

class UserIdentity(models.Model):
    """
    Login User identity: AdminStaff, AdminSystem, Expert, SchoolTeam, visitor,
    Teacher, Student
    """
    identity = models.CharField(max_length=50, blank=False, unique=True,
                                choices=AUTH_CHOICES, default=STUDENT_USER,
                                verbose_name="身份级别")
    auth_groups = models.ManyToManyField(User, related_name="identities")

    class Meta:
        verbose_name = "登录权限"
        verbose_name_plural = "登录权限"

    def __unicode__(self):
        return self.get_identity_display()

class AdminSetting(models.Model):
    school_year=models.ForeignKey(SchoolYear,verbose_name="学年")
    school_term=models.IntegerField(verbose_name="学期")
    tearm_first_day=models.DateTimeField(blank=False,null=True,verbose_name="学期第一天")
    course_select_start=models.DateTimeField(blank=False,null=True,verbose_name="选课开始时间")
    course_select_end=models.DateTimeField(blank=False,null=True,verbose_name="选课结束时间")
    score_enter_start=models.DateTimeField(blank=False,null=True,verbose_name="成绩录入开始时间")
    score_enter_end=models.DateTimeField(blank=False,null=True,verbose_name="成绩录入结束时间")
    course_select_switch=models.BooleanField(null=False,default=False,verbose_name=u"选课开关")
    class_change_switch=models.BooleanField(null=False,default=False,verbose_name=u"转班开关")
    recruit_switch=models.BooleanField(null=False,default=False,verbose_name=u"招新开关")


class ClassRoom(models.Model):
    room_name=models.CharField(blank=False,max_length=30,unique=True,verbose_name=u"教室")
    class Meta:
        verbose_name="教室"
        verbose_name_plural="教室"
    def __unicode__(self):
        return "%s"%(self.room_name)
