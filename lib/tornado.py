from django.conf import settings as django_settings
import django.contrib.auth as django_auth
from django.utils.importlib import import_module

def store_django_user(request_handler):
    request_handler.session = import_module(
        django_settings.SESSION_ENGINE).SessionStore(request_handler.get_cookie(
            django_settings.SESSION_COOKIE_NAME))
    request_handler.user = django_auth.get_user(request_handler)
