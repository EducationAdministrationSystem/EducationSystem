# coding: UTF-8

from django.contrib.auth.models import User
from users.models  import StudentProfile

users=User.objects.all()
for user in users:
    if len(user.username) == 9:
        sts=StudentProfile.objects.filter(userid=user)
        if sts.count() ==0:
            print user
            user.delete()



