"""
WSGI config for DailyFresh project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 通知wsgi服务器setting文件的位置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DailyFresh.settings")

application = get_wsgi_application()
