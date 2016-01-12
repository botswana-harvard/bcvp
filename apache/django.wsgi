############################################
# apache2 needs permission to access this file
# sudo chgrp www-data apache/django.wsgi
# chmod g+x apache/django.wsgi
############################################

import os
import sys
#import site
#import platform

VIRTUALENV_PATH = '/home/django/.virtualenvs/bcvp/'
SOURCE_ROOT_PATH = '/home/django/source/'
LOCAL_PROJECT_RELPATH = 'bcvp/'

# Add the site-packages of the chosen virtualenv to work with
activate_env=os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

# update path
sys.path.insert(0, os.path.join(VIRTUALENV_PATH, 'local/lib/python2.7/site-packages'))
sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, LOCAL_PROJECT_RELPATH))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bcvp.settings'

# Activate the virtual env
#activate_env=os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
#execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
