from common.models import SmallClassPractice


small_class_practice=SmallClassPractice.objects.all()
for scp in small_class_practice:
    for i in range(1,8):
        for j in range(1,7):
            remainFieldName="class_remain_%d_%d"%(i,j)
            setattr(scp,remainFieldName,0)
    scp.save()



