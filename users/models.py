#encoding=utf-8
import datetime,os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from const import PRESIDENT_USER,PRACTICE_USER,TEACHER_USER,STUDENT_USER,SEX_CHOICES,SEX_MALE,DEFAULT_NATION,APARTMENT_CHOICES,COLLEGE_CHOICES,ADMINSTAFF_USER, CLASS_CHOICES,GRADE_CHOICE
from const.models import UserIdentity
# Create your models here.
class PresidentProfile(models.Model):
    userid =models.ForeignKey(User,unique=True,verbose_name=u"用户id")
    class Meta:
        verbose_name="督导账户"
        verbose_name_plural="督导账户"
    def __unicode__(self):
        return '%s' % self.userid
    def save(self,*args,**kwargs):
        super(PresidentProfile,self).save()
        auth,created=UserIdentity.objects.get_or_create(identity=PRESIDENT_USER)
        self.userid.identities.add(auth)
class AdminStaffProfile(models.Model):
    userid =models.ForeignKey(User,unique=True,verbose_name=u"用户id")
    class Meta:
        verbose_name="管理员账户"
        verbose_name_plural="管理员账户"
    def __unicode__(self):
        return '%s' % self.userid
    def save(self,*args,**kwargs):
        super(AdminStaffProfile,self).save()
        auth,created=UserIdentity.objects.get_or_create(identity=ADMINSTAFF_USER)
        self.userid.identities.add(auth)

class PracticeProfile(models.Model):
    userid =models.ForeignKey(User,unique=True,verbose_name=u"用户id")
    nick_name=models.CharField(max_length=20,blank=False,verbose_name=u"简称")
    full_name=models.CharField(max_length=30,blank=False,verbose_name=u"全称")
    #responsible_teacher=models.ForeignKey(TeacherProfile,blank=False,verbose_name=u"负责老师")
    class Meta:
        verbose_name="实践班账户"
        verbose_name_plural="实践班账户"
    def __unicode__(self):
        return '%s' % (self.full_name)
    def save(self,*args,**kwargs):
        super(PracticeProfile,self).save()
        auth,created=UserIdentity.objects.get_or_create(identity=PRACTICE_USER)
        self.userid.identities.add(auth)

class SmallClass(models.Model):
    practice_class = models.ForeignKey(PracticeProfile,blank=False,verbose_name=u"所属实践班")
    class_name = models.CharField(max_length=30,blank=False,verbose_name=u"班级名称")
    brother_class = models.ForeignKey('self')
    class Meta:
        verbose_name="小班"
        verbose_name_plural="小班"
    def __unicode__(self):
        return '%s' % (self.class_name)

class StudentProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    userid = models.ForeignKey(User, unique=True,
                                verbose_name="权限对应ID")
    small_class=models.ForeignKey(SmallClass,blank=True,verbose_name=u"所属班级")
    baseinfo_name = models.CharField(blank=False, max_length=100,
                            verbose_name=u"姓名")
    baseinfo_sex = models.CharField(blank=False, max_length=10,null=True,choices=SEX_CHOICES,default = SEX_MALE,
                            verbose_name=u"性别")
    baseinfo_nation = models.CharField(blank=False, null=True,max_length=100,default=DEFAULT_NATION,
                            verbose_name=u"民族")
    baseinfo_birth = models.DateField(blank=False,null=True, verbose_name=u"生日")
    baseinfo_idcard = models.CharField(blank=False,null=True,  max_length=100,
                            verbose_name=u"身份证")
    baseinfo_studentid = models.CharField(primary_key=True,blank=False, max_length=100,
                            verbose_name=u"学号")
    collegeinfo_apartment = models.IntegerField(blank=False,null=True, choices=APARTMENT_CHOICES,verbose_name=u"学部")
    collegeinfo_college=models.IntegerField(blank=False,null=True, choices=COLLEGE_CHOICES,verbose_name=u"院系")
    collegeinfo_major = models.CharField(blank=True,null=True,max_length=30,verbose_name=u"专业")
    collegeinfo_class = models.CharField(blank = False,null=True, max_length=20, verbose_name=u"班级")
    contactinfo_dormitory = models.CharField(blank=False,null=True, max_length=50,verbose_name=u"宿舍")
    contactinfo_telephone = models.CharField(blank=False,null=True, max_length=20,verbose_name=u"电话")
    contactinfo_email = models.EmailField(verbose_name=u"邮箱",null=True, blank=False)
    innovation_grade = models.IntegerField(blank=False, null=False, max_length=4,
                               default=lambda: datetime.datetime.today().year,
                               verbose_name=u"进入年份")


    class Meta:
        verbose_name = "学生账户"
        verbose_name_plural = "学生账户"
    def __unicode__(self):
        return '%s(%s)' % (self.baseinfo_name, self.userid)
    def get_name(self):
        return '%s' % (self.baseinfo_name)
    def save(self,*args,**kwargs):
        super(StudentProfile,self).save()
        auth,created=UserIdentity.objects.get_or_create(identity=STUDENT_USER)
        self.userid.identities.add(auth)
    def get_export_data(self):
        """
            return data for excel export
        """
        export_data = {}
        export_data[0] = self.baseinfo_name
        export_data[1] = self.baseinfo_studentid
        export_data[2] = self.small_class
        export_data[3] = self.innovation_grade
        export_data[4] = self.get_baseinfo_sex_display()
        export_data[5] = self.get_collegeinfo_college_display()
        export_data[6] = self.contactinfo_email
        export_data[7] = self.contactinfo_telephone
        return export_data


class TeacherProfile(models.Model):
    userid=models.ForeignKey(User,unique=True,verbose_name=u"用户id")
    small_class=models.ForeignKey(SmallClass,blank=True,verbose_name=u"所属班级")
    teacher_id=models.CharField(primary_key=True,blank=False,max_length=50,verbose_name=u"教工号")
    teacher_name=models.CharField(blank=False,max_length=50,verbose_name=u"姓名")
    teacher_email = models.EmailField(verbose_name=u"电子邮件",blank=False)
    teacher_telephone = models.CharField(blank=False,max_length=20,verbose_name=u"电话")
    office_address=models.CharField(blank=False,max_length=50,verbose_name=u"办公室地址")
    office_phone=models.CharField(blank=False,max_length=30,verbose_name=u"办公室电话")
    class Meta:
        verbose_name="教师账户"
        verbose_name_plural="教师账户"
    def __unicode__(self):
        return '%s' % (self.teacher_name)
    def save(self,*args,**kwargs):
        super(TeacherProfile,self).save()
        auth,created=UserIdentity.objects.get_or_create(identity=TEACHER_USER)
        self.userid.identities.add(auth)

def getPractices():
    return tuple((practice.id, practice) for practice in PracticeProfile.objects.all())

class ApplyInfo(models.Model):
    student_name=models.CharField(max_length=20,blank=False,verbose_name=u"姓名")
    sex=models.CharField(max_length=20,blank=False,choices=SEX_CHOICES,verbose_name=u"性别")
    student_id=models.CharField(primary_key=True,max_length=9,blank=False,verbose_name=u"学号")
    tel_num=models.CharField(max_length=20,blank=False,verbose_name=u"电话")
    email=models.EmailField(blank=False,verbose_name=u"邮箱")
    apartment=models.IntegerField(blank=False,choices=APARTMENT_CHOICES,verbose_name=u"学部")
    college=models.IntegerField(blank=False,choices=COLLEGE_CHOICES,verbose_name=u"院系")
    wish_first=models.ForeignKey(PracticeProfile,related_name="wish_first",verbose_name=u"第一志愿")
    wish_second=models.ForeignKey(PracticeProfile,related_name="wish_second",verbose_name=u"第二志愿")
    self_introduction=models.TextField(max_length=600,blank=True,null=True,verbose_name=u"自我介绍")
    innovation_grade = models.IntegerField(blank=False, null=False, max_length=4,
                               default=lambda: datetime.datetime.today().year,
                               verbose_name=u"进入年份")
    class Meta:
        verbose_name = "在线报名表"
        verbose_name_plural = "在线报名表"
    def __unicode__(self):
        return self.student_name
    def get_export_data(self):
        export_data = {}
        export_data[0] = self.student_name
        export_data[1] = self.get_sex_display()
        export_data[2] = self.student_id
        export_data[3] = self.tel_num
        export_data[4] = self.email
        export_data[5] = self.get_apartment_display()
        export_data[6] = self.get_college_display()
        export_data[7] = self.is_first_wish
        return export_data


        
    

