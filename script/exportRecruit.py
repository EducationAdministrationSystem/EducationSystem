# coding:UTF-8
from users.models import ApplyInfo,PracticeProfile

#统计在线报名表中各实践班作为第一志愿的报名学生人数和导出学生名单.txt文件

student_list = []
practiceObj = PracticeProfile.objects.get(full_name = "金融量化对冲研究室")
#创造发明创新实践班　机电创新实践班　数学建模创新实践班　软件创新实践班　媒体技术创新实践班　人形机器人创新实践班　ACM-ICPC创新实践班　
#创业教育创新实践班　智能硬件工作坊　互联网＋工作坊　3D打印工作坊　虚拟现实工作坊　金融量化对冲研究室
# student_list = ApplyInfo.objects.filter(innovation_grade = "2016")
student_list = ApplyInfo.objects.filter(innovation_grade = "2016",wish_first = practiceObj)
print len(student_list)
# outfile = open("../czfm.txt",'w')
# for item in student_list:
#     item = item.student_name.encode("UTF-8") + "\t" + item.student_id.encode("UTF-8") + "\t" + item.tel_num.encode("UTF-8") + "\t" + item.get_apartment_display().encode("UTF-8") + "\t\t" + item.get_college_display().encode("UTF-8") + "\r\n"
#     outfile.write(item)
# outfile.close()
