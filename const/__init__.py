# coding: UTF-8
# APP student
IDENTITYERROR = u"登陆身份有误！"

PAGE_ELEMENTS = 10
DEFAULT_NATION = u"汉族"

SEX_MALE = "male"
SEX_FEMALE = "female"

SEX_CHOICES = (
    (SEX_MALE, u"男"),
    (SEX_FEMALE, u"女"),
)

ADJUST_CHOICES = (
    (0, u"是"),
    (1, u"否"),
)

GRADE_CHOICE=(
    (-1,u"全部"),
    (1,u"一年级"),
    (2,u"二年级"),
    (3,u"三年级"),
)

TERM_CHOICE=(
    (-1,u"全部学期"),
    (1,u"第一学期"),
    (2,u"第二学期"),
)

PAGE_CHOICE = (
    (10, "10"),
    (20, "20"),
    (30, "30"),
    (40, "40"),
    (50, "50"),
)
# APARTMENT_CHOICES = (
# 	(0, '数学科学学院'),
# 	(1, '物理与光电工程学院'),
# 	(2, '化工与环境生命学部'),
# 	(3, '机械工程与材料能源学部'),
# 	(4, '建设工程学部'),
# 	(5, '建筑与艺术学院'),
# 	(6, '运载工程与力学学部'),
# 	(7, '电子信息与电气工程学部'),
# 	(8, '外国语学院'),
# 	(9, '人文与社会科学学部'),
# 	(10, '管理与经济学部'),
#         (11, '创新创业学院'),
# )

PA_CHOICES = (
	(0, '群众'),
	(1, '团员'),
	(2, '党员'),
	(3, '其他'),
)

APARTMENT_CHOICES = (
	(0, '数学科学学院'),
	(1, '物理学院'),
	(2, '化工与环境生命学部'),
	(3, '机械工程学院'),
	(4, '建设工程学部'),
	(5, '建筑与艺术学院'),
	(6, '运载工程与力学学部'),
	(7, '电子信息与电气工程学部'),
	(8, '外国语学院'),
	(9, '人文与社会科学学部'),
	(10, '管理与经济学部'),
    (11, '材料科学与工程学院'),
    (12, '能源与动力学院'),
    (13, '软件学院'),
    (14, '大连理工大学－立命馆大学国际信息软件学院'),
    (15, '光电工程与仪器科学学院'),
    (16, '创新创业学院'),
    (17, '大连理工大学-白俄罗斯国立大学联合学院'),
)


COLLEGE_CHOICES = (
    # 数学
	(0, '数学类'),
    # 物理
	(1, '应用物理学'),
	(2, '应用物理学（王大珩物理科学班）'),
    # 化环生
	(3, '制药工程'),
    (4, '化学工程与工艺(类)'),
    (5, '高分子材料与工程'),
    (6, '应用化学'),
    (7, '应用化学（张大煜化学菁英班）'),
    (8, '过程装备与控制工程（类）'),
    (9, '生物工程'),
    (10, '环境科学与工程类'),
    (11, '化工与制药类（化工环境生命类创新实验班）'),
# 机械
	(12, '机械类'),
	(13, '机械设计制造及其自动化（日语强化）'),
	(14, '机械类（机械类创新实验班）'),
# 建工
	(15, '土木工程（类）'),
	(16, '水利类'),
	(17, '工程管理'),
	(18, '建筑环境与能源应用工程'),
	(19, '交通工程'),
# 建艺
	(20, '建筑学'),
	(21, '城乡规划'),
	(22, '雕塑'),
	(23, '设计学类'),
	(24, '工业设计'),
# 运力
	(25, '船舶与海洋工程'),
	(26, '工程力学'),
	(27, '车辆工程（英语强化）'),
	(28, '飞行器设计与工程'),
	(29, '工程力学（钱令希力学创新实验班）'),
# 电信
	(30, '电气工程及其自动化'),
	(31, '自动化'),
	(32, '电子信息工程（类）'),
    (33, '计算机科学与技术'),
	(34, '计算机科学与技术（日语强化）'),
	(35, '生物医学工程'),
	(36, '电子信息类（电气信息类创新实验班）'),
# 外语
	(37, '英语（类）'),
	(38, '日语'),
	(39, '俄语'),
# 人文
	(40, '公共管理类'),
	(41, '新闻传播学类'),
	(42, '哲学'),
# 管经
	(43, '工商管理类'),
	(44, '信息管理与信息系统'),
	(45, '金融学类'),
#材料
    (46, '材料类'),
    (47, '金属材料工程（日语强化）'),
# 能动
    (48, '能源动力类'),
# 软件
    (49, '软件工程（类）'),
    (50, '软件工程（日语强化）'),
# 立命馆
    (51, '计算机类（中外合作办学）（软件工程）'),
# 微电子
    (52, '集成电路设计与集成系统'),
    (53, '电子科学与技术'),

    (54, '测试'),
# 中白
    (55, '应用物理学'),
    (56, '工程力学'),
# 光仪
    (57,'光电信息科学与工程'),
    (58,'测控技术与仪器'),
)


# COLLEGE_SHORT_CHOICES = (
#     (0, u'数学类'),
#     (1, u'物理学类'),
#     (2, u'应用物理学'),
#     (3, u'制药工程'),
#     (4, u'化工与制药类'),
#     (5, u'高分子材料'),
#     (6, u'无机非金属材料'),
#     (7, u'应用化学'),
#     (8, u'化学工程与工艺'),
#     (9, u'应用化学'),
#     (10, u'过程装备与控制'),
#     (11, u'生物工程类'),
#     (12, u'环境科学与工程类'),
#     (13, u'化工与制药类'),
#     (14, u'材料类'),
#     (15, u'金属材料工程'),
#     (16, u'机械类'),
#     (17, u'机械设计'),
#     (18, u'机械设计'),
#     (19, u'能源动力类'),
#     (20, u'机械类'),
#     (21, u'土木工程'),
#     (22, u'土木工程'),
#     (23, u'水利类'),
#     (24, u'工程管理'),
#     (25, u'建环与能源'),
#     (26, u'交通工程'),
#     (27, u'交通工程（国防生）'),
#     (28, u'建筑学'),
#     (29, u'城乡规划'),
#     (30, u'雕塑（理）'),
#     (31, u'雕塑（文）'),
#     (32, u'设计学类（理）'),
#     (33, u'设计学类（文）'),
#     (34, u'工业设计'),
#     (35, u'船舶与海洋工程'),
#     (36, u'工程力学'),
#     (37, u'车辆工程(英强)'),
#     (38, u'车辆工程(英强)'),
#     (39, u'飞行器设计'),
#     (40, u'工程力学'),
#     (41, u'电气'),
#     (42, u'自动化'),
#     (43, u'电子信息类'),
#     (44, u'电子信息类'),
#     (45, u'集成电路'),
#     (46, u'计算机'),
#     (47, u'计算机(日强)'),
#     (48, u'生物医学工程'),
#     (49, u'电子信息类'),
#     (50, u'英语'),
#     (51, u'日语'),
#     (52, u'俄语'),
#     (53, u'公共管理类(理)'),
#     (54, u'公共管理类(文)'),
#     (55, u'新闻传播学类(理)'),
#     (56, u'新闻传播学类(文)'),
#     (57, u'哲学(理)'),
#     (58, u'哲学(文)'),
#     (59, u'工商管理类'),
#     (60, u'信息管理'),
#     (61, u'金融学类'),
# )
COLLEGE_SHORT_CHOICES = (
	(0, '数学类'),
	(1, '物理学类'),
	(2, '应用物理学'),
	(3, '制药工程'),
    (4, '化学工程与工艺'),
    (5, '高分子材料与工程'),
    (6, '应用化学'),
    (7, '应用化学'),
    (8, '过程装备与控制工程'),
    (9, '生物工程'),
    (10, '环境科学与工程类'),
    (11, '化工与制药类'),
	(12, '机械类'),
	(13, '机械设计制造及其自动化'),
	(14, '机械类'),
	(15, '土木工程'),
	(16, '水利类'),
	(17, '工程管理'),
	(18, '建筑环境与能源应用工程'),
	(19, '交通工程'),
	(20, '建筑学'),
	(21, '城乡规划'),
	(22, '雕塑'),
	(23, '设计学类'),
	(24, '工业设计'),
	(25, '船舶与海洋工程'),
	(26, '工程力学'),
	(27, '车辆工程'),
	(28, '飞行器设计与工程'),
	(29, '工程力学'),
	(30, '电气工程及其自动化'),
	(31, '自动化'),
	(32, '电子信息工程'),
    (33, '计算机科学与技术'),
	(34, '计算机科学与技术'),
	(35, '生物医学工程'),
	(36, '电子信息类'),
	(37, '英语'),
	(38, '日语'),
	(39, '俄语'),
	(40, '公共管理类'),
	(41, '新闻传播学类'),
	(42, '哲学'),
	(43, '工商管理类'),
	(44, '信息管理与信息系统'),
	(45, '金融学类'),
    (46, '材料类'),
    (47, '金属材料工程'),
    (48, '能源动力类'),
    (49, '软件工程'),
    (50, '软件工程'),
    (51, '计算机类'),
    (52, '集成电路设计'),
    (53, '电子科学与技术'),
    (54, '测试'),
    (55, '应用物理学'),
    (56, '工程力学'),
    (57,'光电信息科学与工程'),
    (58,'测控技术与仪器'),
)


COLLEGE_DICT = {
	0: ((0, '数学类'),),

	1: (
	(1, '物理学类'),
	(2, '应用物理学（王大珩物理科学班）'),
	),

	2: (
	(3, '制药工程'),
    (4, '化学工程与工艺(类)'),
    (5, '高分子材料与工程'),
    (6, '应用化学'),
    (7, '应用化学（张大煜化学菁英班）'),
    (8, '过程装备与控制工程（类）'),
    (9, '生物工程'),
    (10, '环境科学与工程类'),
    (11, '化工与制药类（化工环境生命类创新实验班）'),
	),

	3: (
	(12, '机械类'),
	(13, '机械设计制造及其自动化（日语强化）'),
	(14, '机械类（机械类创新实验班）'),
	),

	4: (
	(15, '土木工程（类）'),
	(16, '水利类'),
	(17, '工程管理'),
	(18, '建筑环境与能源应用工程'),
	(19, '交通工程'),
	),

	5: (
	(20, '建筑学'),
	(21, '城乡规划'),
	(22, '雕塑'),
	(23, '设计学类'),
	(24, '工业设计'),
	),

	6: (
	(25, '船舶与海洋工程'),
	(26, '工程力学'),
	(27, '车辆工程（英语强化）'),
	(28, '飞行器设计与工程'),
	(29, '工程力学（钱令希力学创新实验班）'),
	),

	7: (
	(30, '电气工程及其自动化'),
	(31, '自动化'),
	(32, '电子信息工程（类）'),
    (33, '计算机科学与技术'),
	(34, '计算机科学与技术（日语强化）'),
	(35, '生物医学工程'),
	(36, '电子信息类（电气信息类创新实验班）'),
	),

	8: (
	(37, '英语（类）'),
	(38, '日语'),
	(39, '俄语'),
	),

	9: (
	(40, '公共管理类'),
	(41, '新闻传播学类'),
	(42, '哲学'),
	),

	10: (
	(43, '工商管理类'),
	(44, '信息管理与信息系统'),
	(45, '金融学类'),
	),

    11: (
    (46, '材料类'),
    (47, '金属材料工程（日语强化）'),
    ),

    12: (
    (48, '能源动力类'),
    ),

    13: (
    (49, '软件工程（类）'),
    (50, '软件工程（日语强化）'),
    ),

    14: (
    (51, '计算机类（中外合作办学）（软件工程）'),
    ),

    15: (
        (57,'光电信息科学与工程'),
        (58,'测控技术与仪器'),
    ),

    16: (
    (54, '测试'),
    ),

    17: (
    (55, '应用物理学'),
    (56, '工程力学'),
    ),


}

CLASS_CHOICES = (
    (0, "机电实践班"),
    (1, "软件工程实践班"),
    (2, "媒体技术实践班"),
    (3, "数学建模实践班"),
    (4, "ACM-ICPC实践班"),
    (5, "创造发明实践班"),
    (6, "创业教育实践班"),
    (7, "人形机器人实践班"),
)
CLASSTIME_CHOICES=(
    (11,"周一1-2节"),
    (12,"周一3-4节"),
    (13,"周一5-6节"),
    (14,"周一7-8节"),
    (15,"周一9-10节"),
    (16,"周一11节"),
    (21,"周二1-2节"),
    (22,"周二3-4节"),
    (23,"周二5-6节"),
    (24,"周二7-8节"),
    (25,"周二9-10节"),
    (26,"周二11节"),
    (31,"周三1-2节"),
    (32,"周三3-4节"),
    (33,"周三5-6节"),
    (34,"周三7-8节"),
    (35,"周三9-10节"),
    (36,"周三11节"),
    (41,"周四1-2节"),
    (42,"周四3-4节"),
    (43,"周四5-6节"),
    (44,"周四7-8节"),
    (45,"周四9-10节"),
    (46,"周四11节"),
    (51,"周五1-2节"),
    (52,"周五3-4节"),
    (53,"周五5-6节"),
    (54,"周五7-8节"),
    (55,"周五9-10节"),
    (56,"周五11节"),
    (61,"周六1-2节"),
    (62,"周六3-4节"),
    (63,"周六5-6节"),
    (64,"周六7-8节"),
    (65,"周六9-10节"),
    (66,"周六11节"),
    (71,"周日1-2节"),
    (72,"周日3-4节"),
    (73,"周日5-6节"),
    (74,"周日7-8节"),
    (75,"周日9-10节"),
    (76,"周日11节"),
)
CLASSTIME_DICT={
    u"周一1-2节" :11,
    u"周一3-4节" :12,
    u"周一5-6节" :13,
    u"周一7-8节" :14,
    u"周一9-10节":15,
    u"周一11节"  :16,
    u"周二1-2节" :21,
    u"周二3-4节" :22,
    u"周二5-6节" :23,
    u"周二7-8节" :24,
    u"周二9-10节":25,
    u"周二11节"  :26,
    u"周三1-2节" :31,
    u"周三3-4节" :32,
    u"周三5-6节" :33,
    u"周三7-8节" :34,
    u"周三9-10节":35,
    u"周三11节"  :36,
    u"周四1-2节" :41,
    u"周四3-4节" :42,
    u"周四5-6节" :43,
    u"周四7-8节" :44,
    u"周四9-10节":45,
    u"周四11节"  :46,
    u"周五1-2节" :51,
    u"周五3-4节" :52,
    u"周五5-6节" :53,
    u"周五7-8节" :54,
    u"周五9-10节":55,
    u"周五11节"  :56,
    u"周六1-2节" :61,
    u"周六3-4节" :62,
    u"周六5-6节" :63,
    u"周六7-8节" :64,
    u"周六9-10节":65,
    u"周六11节"  :66,
    u"周日1-2节" :71,
    u"周日3-4节" :72,
    u"周日5-6节" :73,
    u"周日7-8节" :74,
    u"周日9-10节":75,
    u"周日11节"  :76,
}
WEEKTIME_CHOICES= [(i,"第%s周" % i) for i in range(1,30)]

ADMINSTAFF_USER = "adminStaff"
PRACTICE_USER = "practice"
TEACHER_USER = "teacher"
STUDENT_USER = "student"
TEACHER_USER = "teacher"
PRESIDENT_USER = "president"

AUTH_CHOICES=(
    (ADMINSTAFF_USER,u"管理员账号"),
    (PRACTICE_USER,u"实践班账号"),
    (TEACHER_USER,u"教师账号"),
    (STUDENT_USER,u"学生账号")
)

AGREE_CHOICE_UNDFINED = 1
AGREE_CHOICE_AGREE = 2
AGREE_CHOICE_REJECT = 3

AGREE_CHOICE=(
    (AGREE_CHOICE_UNDFINED,u"待审核"),
    (AGREE_CHOICE_AGREE,u"同意"),
    (AGREE_CHOICE_REJECT,u"不同意"),
)

GRADE_IGNORE=["1160168010","1160160010"]
