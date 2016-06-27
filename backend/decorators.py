# coding: UTF-8
'''
Created on 2013-04-01

@author: tianwei

Desc: decorators for some controlers, such as time, authorities
'''

import os
import sys
import datetime

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from const import *
from const.models import *
from backend.logging import loginfo


def check_auth(user=None, authority=None):
    """
    if this user(a id object) has this authority, return True, else False
        Arguments:
            In: user, it is user model object
                authority, it is a const string , which can show the
                authorities
            Out:True or False
    """
    if user is None or authority is None or user.is_anonymous() is True:
        return False

    auth_list = user.identities.all()

    try:
        auth = UserIdentity.objects.get(identity=authority)
    except UserIdentity.DoesNotExist, err:
        loginfo(p=err, label="ERROR in check_auth function!!!")
        return False

    for item in auth_list:
        if item.identity == auth.identity:
            return True

    return False


class authority_required(object):
    """
    This decorator will check whether the user is adminstaff
    """
    def __init__(self, identity):
        self.auth = identity

    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            identity = request.session.get('auth_role', "")
            is_passed = False
            loginfo(identity)
            loginfo(self.auth)
            if identity == self.auth:
                is_passed = check_auth(user=request.user, authority=self.auth)
            loginfo(p=is_passed, label="authority_required decorator")
            if is_passed:
                response = method(request, *args, **kwargs)
                return response
            else:
                # TODO: add a custom 403 page
                return HttpResponseRedirect(reverse('backend.errorviews.error403'))
        return wrappered_method
class check_submit_status(object):
    """
    This decorator will deal with application,task,progress,final,the following:
    """
    def __init__(self, phase):
        self.phase = phase
    def get_submit_status(self,pro):
        if self.phase == SUBMIT_STATUS_APPLICATION:
            return pro.project_special.application_status and (pro.project_status.status < PROJECT_STATUS_APPLICATION_COMMIT_OVER and pro.project_status.status >= PROJECT_STATUS_APPLY)
        elif self.phase == SUBMIT_STATUS_TASK:
            return pro.project_special.task_status and (pro.project_status.status < PROJECT_STATUS_TASK_COMMIT_OVER and pro.project_status.status >= PROJECT_STATUS_APPROVAL)
        elif self.phase == SUBMIT_STATUS_PROGRESS:
            return pro.project_special.progress_status and (pro.project_status.status < PROJECT_STATUS_PROGRESS_COMMIT_OVER and pro.project_status.status >= PROJECT_STATUS_TASK_SCHOOL_OVER)
        elif self.phase == SUBMIT_STATUS_FINAL:
            return pro.project_special.final_status and (pro.project_status.status < PROJECT_STATUS_FINAL_COMMIT_OVER and pro.project_status.status >= PROJECT_STATUS_PROGRESS_SCHOOL_OVER)
        elif self.phase == SUBMIT_STATUS_REVIEW:
            pass
        return True
    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            #check time control
            identity = request.session.get('auth_role', "")
            is_submited = False
            if identity == ADMINSTAFF_USER and check_auth(user=request.user, authority=ADMINSTAFF_USER):
                is_submited = True
            elif identity == FINANCE_USER and check_auth(user=request.user, authority=FINANCE_USER):
                is_submited = True
            elif identity == SCHOOL_USER and check_auth(user=request.user, authority=SCHOOL_USER):
                is_submited = True
            elif identity == COLLEGE_USER and check_auth(user=request.user, authority=COLLEGE_USER):
                is_submited = True
            elif identity == EXPERT_USER and check_auth(user=request.user, authority=EXPERT_USER):
                pass
            elif identity == TEACHER_USER and check_auth(user=request.user, authority=TEACHER_USER):
                pro = ProjectSingle.objects.get(project_id = kwargs["pid"])
                loginfo(pro)
                is_submited = self.get_submit_status(pro);
            loginfo(p=is_submited, label="check_submit_status decorator, is_submited")
            kwargs["is_submited"] = is_submited
            response = method(request, *args, **kwargs)
            return response
        return wrappered_method
