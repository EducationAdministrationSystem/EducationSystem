# coding:utf-8
from users.models import ApplyInfo,PracticeProfile
from const import COLLEGE_SHORT_CHOICES

#统计在线报名表中各实践班作为第一志愿的报名学生人数和导出学生名单.txt文件

student_list = []
college_short = dict(COLLEGE_SHORT_CHOICES)
# for item in COLLEGE_SHORT_CHOICES:
#     print item

# practiceObj = PracticeProfile.objects.get(full_name = "金融量化对冲研究室")
practiceObj = PracticeProfile.objects.all()
# print practiceObj

#创造发明创新实践班　机电创新实践班　数学建模创新实践班　软件创新实践班　媒体技术创新实践班　人形机器人创新实践班　ACM-ICPC创新实践班　
#创业教育创新实践班　智能硬件工作坊　互联网＋工作坊　3D打印工作坊　虚拟现实工作坊　金融量化对冲研究室
# student_list = ApplyInfo.objects.filter(innovation_grade = "2016")

for item in practiceObj:
########################################################################################
    student_list = ApplyInfo.objects.filter(innovation_grade = "2017",wish_first = item)
    print "LEN: ", len(student_list)
    filename = '%s%s%s'%("recruit_final/", item.full_name, ".csv")
    print filename
    outfile = open(filename,'w')
    import csv
    writer = csv.writer(outfile)
    writer.writerow(["姓名", "学号", "性别", "电话", "院系", "专业", "第一志愿", "第二志愿", "是否调剂"])
    for item in student_list:
        name = item.student_name.encode("UTF-8").ljust(14)
        stuid = item.student_id.encode("UTF-8").ljust(10)
        sex = item.get_sex_display().encode("UTF-8").ljust(2)
        tel = item.tel_num.encode("UTF-8").ljust(12)
        apartment = item.get_apartment_display().encode("UTF-8").ljust(40)
        college = college_short[item.college].ljust(40)
        first = item.wish_first.full_name.encode("UTF-8").ljust(40)
        second = item.wish_second.full_name.encode("UTF-8").ljust(40)
        adjust = item.get_ifAdujst_display().encode("UTF-8").ljust(2)
        writer.writerow([name, stuid, sex, tel, apartment, college, first, second, adjust])
        # info = name+"\t"+stuid+"\t"+sex+"\t"+tel+"\t"+apartment+"\t"+college+"\t"+first+"\t"+second+"\t"+adjust+"\r\n"
        # outfile.write(info)
    outfile.close()
