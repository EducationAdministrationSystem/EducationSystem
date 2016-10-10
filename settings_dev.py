"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: Django setting for daily development
    Created: 2013-4-12
"""
from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tempdatabase',             # Or path to database file if using sqlite3.
        #'NAME': 'EducationSystem',
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'root',                   # Not used with sqlite3.
        'HOST': '192.168.2.81',                           # Set to empty string for localhost. Not used with sqlite3.
        #'HOST':'192.168.20.106',
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'EducationSystem',             # Or path to database file if using sqlite3.
#         'USER': 'root',                       # Not used with sqlite3.
#         'PASSWORD': 'root',                   # Not used with sqlite3.
#         'HOST': '192.168.20.106',                           # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
#     }
# }

# Website settings
WEB_TITLE = "Province Management Dev"
