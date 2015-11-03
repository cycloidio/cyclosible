"""
WSGI config for Cyclosible project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

from ws4redis.uwsgi_runserver import uWSGIWebsocketServer
import os
import gevent.socket
import redis.connection


redis.connection.socket = gevent.socket
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Cyclosible.settings")
application = uWSGIWebsocketServer()
