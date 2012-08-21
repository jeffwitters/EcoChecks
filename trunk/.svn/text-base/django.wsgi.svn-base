import os
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp/python-egs/'
sys.path.append('/var/www/vhosts/ecochecks.org/app')
sys.path.append('/var/www/vhosts/ecochecks.org/app/ecochecks')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecochecks.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


