# coding: UTF-8
from adminStaff.utility import xls_info_course
from common.models import Course

courses =Course.objects.all()
xls_info_course(1,courses)
