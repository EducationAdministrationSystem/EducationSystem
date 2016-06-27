# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from backend.decorators import check_auth
from django.contrib.auth import logout
from backend.logging import loginfo
from django.shortcuts import render_to_response
from django.template import RequestContext
from const import ADMINSTAFF_USER
def loginviews(request):
    return render(request,"login.html")

def login_redirect(request,identity):
    """
    When the user login, it will decide to jump the according page, in other
    words, school user will be imported /school/ page, if the user have many
    authorities, the system will jump randomly
    """
    #TODO: I will use reverse function to redirect, like school and expert

    
    loginfo(identity)
    if check_auth(request.user,identity):
        loginfo(request.user)
        pass
    else:
        try:
            del request.session['auth_role']
        except:
            pass
        logout(request)
        return HttpResponseRedirect('/identityerror')
    if identity==ADMINSTAFF_USER:
        redirect_url = '/'+identity+'/'+"studentmanage"
    else:
        redirect_url = '/'+identity+'/'+"homepage"
    request.session['auth_role'] = identity
    return HttpResponseRedirect(redirect_url)

def logout_redirect(request):
    try:
        del request.session['auth_role']
    except KeyError:
        pass
    return HttpResponseRedirect('/')
