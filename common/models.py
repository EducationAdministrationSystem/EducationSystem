# coding: UTF-8
from const import *
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from const.models import ClassTime,WeekTime,SchoolYear,ClassRoom
from users.models import StudentProfile,PracticeProfile,TeacherProfile,SmallClass
import datetime

# Create your models here.
class CoursePlan(models.Model):
    course_plan_id=models.CharField(unique=True,max_length=50,blank=False,verbose_name=u"课程ID")
    course_name=models.CharField(max_length=50,blank=False,verbose_name=u"课程名称")
    course_grade=models.IntegerField(blank=False,choices=GRADE_CHOICE,verbose_name=u"年级")
    course_term=models.IntegerField(blank=False,choices=TERM_CHOICE,verbose_name=u"学期")
    #course_point=models.IntegerField(blank=False,verbose_name=u"学分")
    course_point=models.DecimalField(blank=False,max_digits=2,decimal_places=1,verbose_name=u"学分")
    course_practice=models.ForeignKey(PracticeProfile,verbose_name=u"所属实践班")
    class Meta:
        verbose_name = u"培养计划"
        verbose_name_plural = u"培养计划"
    def __unicode__(self):
        return '%s'% (self.course_name)

class Course(models.Model):
    """
    """
    course_id = models.ForeignKey(CoursePlan,verbose_name=u"课程计划")
    teacher = models.ForeignKey(TeacherProfile,verbose_name=u"教师")
    class_week = models.ManyToManyField(WeekTime,blank=True,verbose_name=u"上课周")
    class_time= models.ManyToManyField(ClassTime,blank=True,verbose_name=u"上课时间")
    class_place= models.ForeignKey(ClassRoom,verbose_name=u"上课地点")
    course_to_class=models.ManyToManyField(SmallClass,blank=True,verbose_name=u"对应小班")
    practice_periods = models.IntegerField(blank=False,default = 0,verbose_name=u"实践学时")
    theory_periods = models.IntegerField(blank=False,default = 0,verbose_name=u"理论学时")
    class_capacity = models.IntegerField(blank=False,default = 0,verbose_name=u"课容量")
    int_nelepeo = models.IntegerField(blank=False,default = 0,verbose_name=u"已选人数")
    attendance_rate = models.IntegerField(blank = False, default = 0, verbose_name = u"考勤分数比例", validators = [MaxValueValidator(100), MinValueValidator(0)])
    homework_rate = models.IntegerField(blank = False, default = 0, verbose_name = u"平时作业比例", validators = [MaxValueValidator(100), MinValueValidator(0)])
    final_rate = models.IntegerField(blank = False, default = 0, verbose_name = u"期末作业比例", validators = [MaxValueValidator(100), MinValueValidator(0)])
    start_year = models.ForeignKey(SchoolYear,blank=False,verbose_name=u"开课学年")
    is_finished = models.BooleanField(null=False,default =False,verbose_name=u"成绩提交完成")

    student = models.ManyToManyField(StudentProfile, through="SelectCourse")
    class Meta:
        verbose_name = u"课程时间表"
        verbose_name_plural = u"课程时间表"
    def __unicode__(self):
        return '%s'% (self.course_id.course_name)
    def get_class_time_display(self):
        return ','.join([unicode(i) for i in self.class_time.all()])
    def get_class_week_display(self):
        return ','.join([str(i.category) for i in self.class_week.all()])
    def calculate_score(self, var_1, var_2, var_3):
        return (var_1 * self.attendance_rate + var_2 * self.homework_rate + var_3 * self.final_rate) / 100
    def get_class_week_list(self,weekstr):
        weeks=[]
        for item in weekstr.split(u","):
            if "-" in item:
                [weeks.append(i) for i in range(int(item.split("-")[0]),int(item.split("-")[1])+1)]
            else:
                weeks.append(int(item))
        return weeks

    def get_export_data(self):
        """
            return data for excel export
        """
        export_data = {}
        export_data[0]  = self.course_id
        export_data[1]  = self.course_id.course_plan_id
        export_data[2]  = self.teacher
        export_data[3]  = self.get_class_week_display()
        export_data[4]  = self.get_class_time_display()
        export_data[5]  = self.class_place
        export_data[6]  = self.practice_periods+self.theory_periods
        export_data[7]  = self.practice_periods
        export_data[8]  = self.theory_periods
        export_data[9]  = self.class_capacity
        export_data[10] = self.int_nelepeo
        export_data[11] = self.course_id.course_point
        export_data[12] = self.course_id.get_course_grade_display()
        export_data[13] = self.start_year
        export_data[14] = self.course_id.get_course_term_display()
        export_data[15] = self.course_id.course_practice
        return export_data


class SelectCourse(models.Model):
    student=models.ForeignKey(StudentProfile,blank=False,verbose_name=u"学生")
    course=models.ForeignKey(Course,blank=False,verbose_name=u"课程")
    evalution=models.CharField(max_length=500,verbose_name=u"教学评估")
    # flag=models.BooleanField(default=False,verbose_name=u"评估状态")
    class Meta:
        verbose_name = u"选课"
        verbose_name_plural = u"选课"
        unique_together = (("student", "course", ), )
    def __unicode__(self):
        return "%s select %s" % (self.student.baseinfo_name, self.course.course_id.course_name)



class Score(models.Model):
    select_obj = models.ForeignKey(SelectCourse)
    attendance = models.IntegerField(blank = False, default = 0, verbose_name = u"考勤分数", validators = [MaxValueValidator(100), MinValueValidator(0)])
    homework = models.IntegerField(blank = False, default = 0, verbose_name = u"平时作业", validators = [MaxValueValidator(100), MinValueValidator(0)])
    final = models.IntegerField(blank = False, default = 0, verbose_name =u"期末评测", validators = [MaxValueValidator(100), MinValueValidator(0)])
    total = models.IntegerField(blank = False, default = 0, verbose_name =u"总分", validators = [MaxValueValidator(100), MinValueValidator(0)])
    class Meta:
        verbose_name = u"分数"
        verbose_name_plural = u"分数"
    def get_simple_export_data(self):
        export_data = {}
        export_data[0] = self.select_obj.student
        export_data[1] = self.total
        return export_data
    def get_export_data(self):
        export_data = {}

        export_data[0] = self.select_obj.student.baseinfo_studentid
        export_data[1] = self.select_obj.student.get_name()
        try:
            export_data[2] = COLLEGE_SHORT_CHOICES[self.select_obj.student.collegeinfo_college][1].decode('utf-8')
        except:
            export_data[2] = ""
        export_data[3] = self.total
        return export_data
    def get_all_data(self):
        export_data = {}
        export_data[0] = self.select_obj.student.baseinfo_studentid
        export_data[1] = self.select_obj.student
        export_data[2] = self.select_obj.course.course_id.course_plan_id
        export_data[3] = self.select_obj.course
        export_data[4] = self.select_obj.course.start_year
        export_data[5] = self.select_obj.course.course_id.course_term
        export_data[6] = self.total
        return export_data

    def __unicode__(self):
        return "%s select %s" % (self.select_obj.student.baseinfo_name, self.select_obj.course.course_id.course_name)

class PracticeClassPractice(models.Model):
    student = models.ForeignKey(StudentProfile, unique=True,verbose_name=u"学生")
    class_select_1_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一1")
    class_select_1_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一2")
    class_select_1_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一3")
    class_select_1_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一4")
    class_select_1_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一5")
    class_select_1_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周一6")

    class_select_2_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二1")
    class_select_2_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二2")
    class_select_2_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二3")
    class_select_2_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二4")
    class_select_2_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二5")
    class_select_2_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周二6")

    class_select_3_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三1")
    class_select_3_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三2")
    class_select_3_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三3")
    class_select_3_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三4")
    class_select_3_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三5")
    class_select_3_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周三6")

    class_select_4_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四1")
    class_select_4_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四2")
    class_select_4_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四3")
    class_select_4_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四4")
    class_select_4_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四5")
    class_select_4_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周四6")

    class_select_5_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五1")
    class_select_5_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五2")
    class_select_5_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五3")
    class_select_5_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五4")
    class_select_5_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五5")
    class_select_5_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周五6")

    class_select_6_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六1")
    class_select_6_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六2")
    class_select_6_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六3")
    class_select_6_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六4")
    class_select_6_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六5")
    class_select_6_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周六6")

    class_select_7_1 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日1")
    class_select_7_2 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日2")
    class_select_7_3 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日3")
    class_select_7_4 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日4")
    class_select_7_5 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日5")
    class_select_7_6 = models.BooleanField(blank = False, default = False, verbose_name = "课余量周日6")
    class Meta:
        verbose_name = u"实践选课"
        verbose_name_plural = u"实践选课"


class Homework(models.Model):
    course = models.ForeignKey(Course,blank=False,verbose_name=u"所属课程")
    name = models.CharField(blank=False, max_length=50, verbose_name=u"作业名称")
    required = models.CharField(blank=False, max_length=500,  verbose_name=u"作业要求")
    deadline = models.DateTimeField(blank=False, verbose_name=u"作业截至时间")
    homework_rank=models.IntegerField(verbose_name=u"作业次序")
    is_final=models.BooleanField(verbose_name=u"是否是期末作业",default=False)
    def __unicode__(self):
        return '%s'% (self.name)
    class Meta:
        verbose_name = u"作业"
        verbose_name_plural = u"作业"

class HomeworkSubmit(models.Model):
    homework = models.ForeignKey(Homework,blank=False,verbose_name=u"所属作业")
    student = models.ForeignKey(StudentProfile, blank=False, verbose_name=u"所属学生")
    homework_file = models.FileField(upload_to = 'tmp/%Y/%m/%d', verbose_name="作业文件")
    score = models.IntegerField(blank = True, null = True, verbose_name="作业评分")
    submit_time = models.DateTimeField(blank=False, verbose_name=u"作业提交时间")
    class Meta:
        verbose_name = u"作业提交"
        verbose_name_plural = u"作业提交"

class SmallClassPractice(models.Model):
    small_class=models.ForeignKey(SmallClass,blank=False,verbose_name=u"所属小班")
    class_grade=models.IntegerField(choices=GRADE_CHOICE,verbose_name=u"年级",default=1)
    class_remain_1_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一1", validators = [MinValueValidator(0)])
    class_remain_1_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一2", validators = [MinValueValidator(0)])
    class_remain_1_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一3", validators = [MinValueValidator(0)])
    class_remain_1_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一4", validators = [MinValueValidator(0)])
    class_remain_1_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一5", validators = [MinValueValidator(0)])
    class_remain_1_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周一6", validators = [MinValueValidator(0)])

    class_remain_2_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二1", validators = [MinValueValidator(0)])
    class_remain_2_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二2", validators = [MinValueValidator(0)])
    class_remain_2_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二3", validators = [MinValueValidator(0)])
    class_remain_2_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二4", validators = [MinValueValidator(0)])
    class_remain_2_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二5", validators = [MinValueValidator(0)])
    class_remain_2_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周二6", validators = [MinValueValidator(0)])

    class_remain_3_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三1", validators = [MinValueValidator(0)])
    class_remain_3_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三2", validators = [MinValueValidator(0)])
    class_remain_3_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三3", validators = [MinValueValidator(0)])
    class_remain_3_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三4", validators = [MinValueValidator(0)])
    class_remain_3_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三5", validators = [MinValueValidator(0)])
    class_remain_3_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周三6", validators = [MinValueValidator(0)])

    class_remain_4_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四1", validators = [MinValueValidator(0)])
    class_remain_4_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四2", validators = [MinValueValidator(0)])
    class_remain_4_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四3", validators = [MinValueValidator(0)])
    class_remain_4_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四4", validators = [MinValueValidator(0)])
    class_remain_4_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四5", validators = [MinValueValidator(0)])
    class_remain_4_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周四6", validators = [MinValueValidator(0)])

    class_remain_5_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五1", validators = [MinValueValidator(0)])
    class_remain_5_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五2", validators = [MinValueValidator(0)])
    class_remain_5_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五3", validators = [MinValueValidator(0)])
    class_remain_5_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五4", validators = [MinValueValidator(0)])
    class_remain_5_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五5", validators = [MinValueValidator(0)])
    class_remain_5_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周五6", validators = [MinValueValidator(0)])

    class_remain_6_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六1", validators = [MinValueValidator(0)])
    class_remain_6_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六2", validators = [MinValueValidator(0)])
    class_remain_6_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六3", validators = [MinValueValidator(0)])
    class_remain_6_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六4", validators = [MinValueValidator(0)])
    class_remain_6_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六5", validators = [MinValueValidator(0)])
    class_remain_6_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周六6", validators = [MinValueValidator(0)])

    class_remain_7_1 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日1", validators = [MinValueValidator(0)])
    class_remain_7_2 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日2", validators = [MinValueValidator(0)])
    class_remain_7_3 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日3", validators = [MinValueValidator(0)])
    class_remain_7_4 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日4", validators = [MinValueValidator(0)])
    class_remain_7_5 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日5", validators = [MinValueValidator(0)])
    class_remain_7_6 = models.IntegerField(blank = False, default = 0, verbose_name = "课余量周日6", validators = [MinValueValidator(0)])
    class Meta:
        verbose_name=u"小班课余量"
        verbose_name_plural=u"小班课余量"
    def __unicode__(self):
        grade = u''
        if self.class_grade == 1: grade = u'一'
        elif self.class_grade == 2: grade = u'二'
        else: grade = u'三'
        return u'%s (%s年级)' % (self.small_class, grade)
