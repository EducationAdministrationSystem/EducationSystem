from common.models import Score
from common.models import SelectCourse

select_set=SelectCourse.objects.filter(course__course_id__course_plan_id="1160165030")

for item in select_set:
    if Score.objects.filter(select_obj=item).count() ==0 :
        s=Score(select_obj=item,attendance=0,homework=0,final=0,total=0)
        s.save()


