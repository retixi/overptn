"""
WSGI config for ptn_ana_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "overptn.settings")

application = get_wsgi_application()

import os,sys,django
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import  WSGIHandler


# sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "overptn.settings")  #变量testproject.settings为django项目下的settings

django.setup()     #避免在虚拟环境下找不到django的app

application = WSGIHandler()