"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: main settings of Chemistry Tools Site
    Created: 2013-3-10
"""

from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from dajaxice.core import dajaxice_autodiscover, dajaxice_config

dajaxice_autodiscover()

#display django admin page
admin.autodiscover()

#Custome error page
handler500 = 'backend.errorviews.error500'
handler403 = 'backend.errorviews.error403'
handler404 = 'backend.errorviews.error404'


urlpatterns = patterns('',
    # Add this to get widgets.AdminDateWidget() working for non is_staff, is_superuser
    # This must be placed before (r'^admin/(.*)', admin.site.root), as that gobals up everything
    url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog'),
    #url(
        #r'^$',
        #include('home.urls'),
        #name="home"
    #),
    url(
        r'^',
        include('registration.urls')

    ),
    url(
        r'^adminStaff/',
        include('adminStaff.urls'),
        name="adminStaff"

    ),
    url(
        r'^practice/',
        include('practice.urls'),
    ),
    url(
        r'^teacher/',
        include('teacher.urls'),
    ),
    url(
        r'^student/',
        include('student.urls'),
    ),
    url(
        r'^recruit/',
        include('recruit.urls'),
    ),
    url(
        r'^admin/',
        include(admin.site.urls),
    ),
    url(
        r'^errors/',
        include("backend.urls"),
    ),
    url(
        r'^president/',
        include('president.urls'),
    )
)

urlpatterns += patterns('', url(r'tinymce/', include('tinymce.urls')),)
urlpatterns += patterns('', url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),)
urlpatterns += staticfiles_urlpatterns()

# for develop to serve user-upload content in MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'media/(?P<path>.*)$',
                'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
                )
