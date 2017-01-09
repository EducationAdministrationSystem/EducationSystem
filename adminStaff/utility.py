# coding: UTF-8

import xlwt,xlrd,os,sys
import datetime
from common.models import CoursePlan,Course
from const.models import *
from users.models import TeacherProfile
from backend.logging import loginfo
from settings import TMP_FILES_PATH,MEDIA_URL
from const import COLLEGE_SHORT_CHOICES

def cell_style(horizontal,vertical):
    """
    为CELL添加水平居中和垂直居中
    """
    alignment = xlwt.Alignment()
    if horizontal:
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    elif vertical:
        alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    return style

def cell_style_border(horizontal,vertical):
    """
    为CELL添加水平居中和垂直居中和边框
    """
    alignment = xlwt.Alignment()
    if horizontal:
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    elif vertical:
        alignment.vert = xlwt.Alignment.VERT_CENTER
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    style.borders = borders
    return style

def cell_style_underline(horizontal,vertical):
    """
    为CELL添加水平居中和垂直居中和下划线
    """
    alignment = xlwt.Alignment()
    if horizontal:
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    elif vertical:
        alignment.vert = xlwt.Alignment.VERT_CENTER
    font = xlwt.Font()
    font.name = 'SimSun'
    font.underline = True
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    style.font = font
    return style

def cell_style_height(horizontal,vertical):
    """
    为表名添加水平居中和垂直居中和下划线，设置字体大小
    """
    alignment = xlwt.Alignment()
    if horizontal:
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    elif vertical:
        alignment.vert = xlwt.Alignment.VERT_CENTER
    font = xlwt.Font()
    font.name = 'SimSun'
    font.underline = True
    font.height = 360
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    style.font = font
    return style


def red_style():
    style = xlwt.XFStyle() # Create Style
    pattern = xlwt.Pattern()
    pattern.pattern = pattern.SOLID_PATTERN
    pattern.pattern_back_colour = 2 #red
    pattern.pattern_fore_colour = 2
    style.pattern = pattern
    return style

def xls_info_course_gen(request,head_list,excelname,extra_data = None):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style_border(horizontal=True,vertical=True)
    style1 = cell_style_height(horizontal=True,vertical=True)
    # generate header
    num = len(head_list)
    worksheet.write_merge(0, 0, 0, num-1,excelname,style1)
    row = 1
    if extra_data != None:
        row = add_extra_data(worksheet,workbook,extra_data)
    # generate body
    for i in range(0,num):
        worksheet.write(row,i,head_list[i],style)

    return worksheet, workbook,row
def get_score_xls_path(request,head_list,obj_set,excelname, func_str = "get_export_data",extra_data = None,extra_foot_data = None):
    """
        function:   generate excel
        @head_list: a dict the head for excel
        @obj_set:   object set each object is a dict
        @excelname: title for excel
    """

    xls_obj, workbook ,row= xls_info_course_gen(request,head_list,excelname,extra_data)
    num = len(head_list)
    row += 1
    count = 0
    score_num = len(obj_set)
    i = 0
    style = cell_style_border(horizontal=True,vertical=True)
    while i<score_num:
        item_datas1 = getattr(obj_set[i], func_str)()
        item_datas2 = []
        xls_obj.write(row, 0, i+1,style)
        if i+1>=score_num:item_datas2 = ['','','','']
        else:
            item_datas2 = getattr(obj_set[i+1], func_str)()
            xls_obj.write(row, 5, i+2,style)
        try:
            for j in range(0,4):
                xls_obj.write(row, j+1, unicode(item_datas1[j]),style)
                xls_obj.write(row, j+6, unicode(item_datas2[j]),style)
        except Exception,e:
            print e
            pass
        finally:
            row+= 1
        i += 2
    xls_obj.col(0).width = 1300
    xls_obj.col(1).width = 2600
    xls_obj.col(2).width = 2000
    xls_obj.col(3).width = 3500
    xls_obj.col(4).width = 1300
    xls_obj.col(5).width = 1300
    xls_obj.col(6).width = 2600
    xls_obj.col(7).width = 2000
    xls_obj.col(8).width = 3500
    xls_obj.col(9).width = 1300

    if extra_foot_data != None:
        add_foot_data(xls_obj, workbook ,extra_foot_data,row)

    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), u"年创新创业学院"+excelname))
    workbook.save(save_path)
    ret_path = os.path.join(MEDIA_URL+"tmp", "%s%s.xls" % (str(datetime.date.today().year), u"年创新创业学院"+excelname))
    return ret_path

def get_xls_path(request,head_list,obj_set,excelname, func_str = "get_export_data",extra_data = None):
    """
        function:   generate excel
        @head_list: a dict the head for excel
        @obj_set:   object set each object is a dict
        @excelname: title for excel
    """

    xls_obj, workbook ,row= xls_info_course_gen(request,head_list,excelname,extra_data)
    num = len(head_list)
    row += 1
    style = cell_style_border(horizontal=True,vertical=True)
    for item in obj_set:
        item_datas = getattr(item, func_str)()
        for i in range(num):
            xls_obj.write(row, i, unicode(item_datas[i]), style)
        row += 1
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), u"年创新创业学院"+excelname))
    save_path.replace('/', '')
    workbook.save(save_path)
    ret_path = os.path.join(MEDIA_URL+"tmp", "%s%s.xls" % (str(datetime.date.today().year), u"年创新创业学院"+excelname))
    return ret_path

ROW_DICT={
    "course_id"       :1,
    "teacher"         :5,
    "class_week"      :8,
    "class_time"      :9,
    "class_place"     :10,
    "course_to_class" :-1,
    "practice_periods":4,
    "theory_periods"  :3,
    "class_capacity"  :7,
    "start_year"      :11,
}
def add_foot_data(worksheet, workbook,extra_data,row):
    style = cell_style_border(horizontal=True,vertical=True)
    worksheet.write_merge(row,row+2,0,0,"备注",style)
    worksheet.write(row,1,"90-100(优)",style)
    worksheet.write(row,2,extra_data[0],style)
    worksheet.write(row,3,"60-69(及格)",style)
    worksheet.write_merge(row,row,4,6,extra_data[3],style)
    worksheet.write(row,7,"旷考",style)
    worksheet.write_merge(row,row,8,9,extra_data[6],style)
    worksheet.write(row+1,1,"80-89(良)",style)
    worksheet.write(row+1,2,extra_data[1],style)
    worksheet.write(row+1,3,"不足60(不及格)",style)
    worksheet.write_merge(row+1,row+1,4,6,extra_data[4],style)
    worksheet.write(row+1,7,"舞弊",style)
    worksheet.write_merge(row+1,row+1,8,9,"",style)
    worksheet.write(row+2,1,"70-79(中)",style)
    worksheet.write(row+2,2,extra_data[2],style)
    worksheet.write(row+2,3,"平均分",style)
    worksheet.write_merge(row+2,row+2,4,6,extra_data[5],style)
    worksheet.write(row+2,7,"合计",style)
    worksheet.write_merge(row+2,row+2,8,9,extra_data[7],style)
    # worksheet.write_merge(row+3, row+4, 0, 3,"1、需用墨水填写，不得污损或涂改，如有更正需复以说明并签字。")
    worksheet.write(row+3,4,"任课教师签字：")
    worksheet.write(row+4,4,"基地负责人签字：")
    # worksheet.write_merge(row+5,row+6,0,3,"2、本表应于7月24日交创新时延学院办公室一份，另一份存教研室。")
    worksheet.write(row+5,4,"创新创业学院签字：")


def add_extra_data(worksheet, workbook, extra_data):
    style = cell_style_underline(horizontal=True,vertical=True)
    style1 = cell_style(horizontal=True,vertical=True)
    worksheet.write_merge(2,2,0,1,extra_data[0],style)
    worksheet.write(2,2,"基地",style1)
    worksheet.write(2,3,"课号：",style1)
    worksheet.write_merge(2,2,4,5,extra_data[1],style)
    worksheet.write(2,7,"课程名称：",style1)
    worksheet.write(2,8,extra_data[2],style)
    worksheet.write_merge(3,3,0,1,extra_data[3],style)
    worksheet.write(3,2,"学年",style1)
    worksheet.write(3,3,extra_data[4],style)
    worksheet.write(3,4,"学期",style1)
    worksheet.write(3,6,"任课教师",style1)
    worksheet.write(3,7,extra_data[5],style)
    worksheet.write(3,8,"学分:",style1)
    worksheet.write(3,9,str(extra_data[6]),style)
    return extra_data[-1]

def xls_import_course(path):
    workbook = xlrd.open_workbook(path)
    table = workbook.sheet_by_index(0)

    wbook = xlwt.Workbook(encoding='utf-8')
    wsheet = wbook.add_sheet('sheet1')
    wsheet.write(0, 0,u"序号")
    wsheet.write(0, 1,u"课程编号")
    wsheet.write(0, 2,u"课程名称")
    wsheet.write(0, 3,u"讲课学时")
    wsheet.write(0, 4,u"实验学时")
    wsheet.write(0, 5,u"教师编号")
    wsheet.write(0, 6,u"教师")
    wsheet.write(0, 7,u"课容量")
    wsheet.write(0, 8,u"上课起止周")
    wsheet.write(0, 9,u"上课时间")
    wsheet.write(0, 10,u"上课地点")
    wsheet.write(0, 11,u"开课学年")
    redstyle = red_style()

    errors= []
    course_list = []
    for i in range(1,table.nrows):
        row = table.row_values(i)
        course = Course()
        try:
            course.course_id = CoursePlan.objects.get(course_plan_id = row[ROW_DICT["course_id"]])
            if course.course_id.course_name != row[ROW_DICT["course_id"]+1].strip():
                raise ValueError('')
            wsheet.write(i,ROW_DICT["course_id"],row[ROW_DICT["course_id"]])
            wsheet.write(i,ROW_DICT["course_id"]+1,row[ROW_DICT["course_id"]+1])
        except:
            errors.append([i,ROW_DICT["course_id"]])
            errors.append([i,ROW_DICT["course_id"]+1])
            wsheet.write(i,ROW_DICT["course_id"],row[ROW_DICT["course_id"]],redstyle)
            wsheet.write(i,ROW_DICT["course_id"]+1,row[ROW_DICT["course_id"]+1],redstyle)
        try:
            course.practice_periods = int(row[ROW_DICT["practice_periods"]])
            wsheet.write(i,ROW_DICT["practice_periods"],row[ROW_DICT["practice_periods"]])
        except:
            errors.append([i,row[ROW_DICT["practice_periods"]]])
            wsheet.write(i,ROW_DICT["practice_periods"],row[ROW_DICT["practice_periods"]],redstyle)
        try:
            course.theory_periods = int(row[ROW_DICT["theory_periods"]])
            wsheet.write(i,ROW_DICT["theory_periods"],row[ROW_DICT["theory_periods"]])
        except:
            errors.append([i,row[ROW_DICT["theory_periods"]]])
            wsheet.write(i,ROW_DICT["theory_periods"],row[ROW_DICT["theory_periods"]],redstyle)
        try:
            course.teacher = TeacherProfile.objects.get(teacher_id = row[ROW_DICT["teacher"]])
            if course.teacher.teacher_name != row[ROW_DICT["teacher"]+1]:
                raise ValueError('')
            wsheet.write(i,ROW_DICT["teacher"],row[ROW_DICT["teacher"]])
            wsheet.write(i,ROW_DICT["teacher"]+1,row[ROW_DICT["teacher"]+1])
        except:
            errors.append([i,ROW_DICT["teacher"]])
            errors.append([i,ROW_DICT["teacher"]+1])
            wsheet.write(i,ROW_DICT["teacher"],row[ROW_DICT["teacher"]],redstyle)
            wsheet.write(i,ROW_DICT["teacher"]+1,row[ROW_DICT["teacher"]+1],redstyle)
        try:
            course.class_capacity = int(row[ROW_DICT["class_capacity"]])
            wsheet.write(i,ROW_DICT["class_capacity"],row[ROW_DICT["class_capacity"]])
        except:
            errors.append([i,ROW_DICT["class_capacity"]])
            wsheet.write(i,ROW_DICT["class_capacity"],row[ROW_DICT["class_capacity"]],redstyle)
        try:
            course.class_place = ClassRoom.objects.get(room_name=row[ROW_DICT["class_place"]])
            wsheet.write(i,ROW_DICT["class_place"],row[ROW_DICT["class_place"]])
        except:
            errors.append([i,ROW_DICT["class_place"]])
            wsheet.write(i,ROW_DICT["class_place"],row[ROW_DICT["class_place"]],redstyle)
        try:
            course.start_year = SchoolYear.objects.get(school_year=row[ROW_DICT["start_year"]])
            wsheet.write(i,ROW_DICT["start_year"],row[ROW_DICT["start_year"]])
        except:
            errors.append([i,ROW_DICT["start_year"]])
            wsheet.write(i,ROW_DICT["start_year"],row[ROW_DICT["start_year"]],redstyle)
        try:
            weeks = WeekTime.objects.filter(category__in = course.get_class_week_list(row[ROW_DICT["class_week"]]))
            wsheet.write(i,ROW_DICT["class_week"],row[ROW_DICT["class_week"]])
        except:
            errors.append([i,ROW_DICT["class_week"]])
            wsheet.write(i,ROW_DICT["class_week"],row[ROW_DICT["class_week"]],redstyle)
        try:
            ts=[]
            for t in row[ROW_DICT["class_time"]].split(','):
                ts.append(CLASSTIME_DICT[t])
            times = ClassTime.objects.filter(category__in = ts)
            wsheet.write(i,ROW_DICT["class_time"],row[ROW_DICT["class_time"]])
        except:
            errors.append([i,ROW_DICT["class_time"]])
            wsheet.write(i,ROW_DICT["class_time"],row[ROW_DICT["class_time"]],redstyle)
        try:
            course_list.append([course,weeks,times])
        except:
            pass
    if len(errors) == 0:
        for item,weeks,times in course_list:
            item.save()
            [item.class_week.add(i) for i in weeks]
            [item.class_time.add(i) for i in times]
        return (True,None)
    else:
        save_path = "".join(path.split('.')[:-1])+".xls"
        wbook.save(save_path)
        return (False,save_path)
