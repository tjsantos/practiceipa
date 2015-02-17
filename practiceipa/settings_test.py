# Testing
# override config when running tests:
#   - logging, static files, media

from .settings import *
from django.conf import global_settings

# set back to defaults
# TODO: refactor using strings and attribute lookup
LOGGING = global_settings.LOGGING
STATICFILES_STORAGE = global_settings.STATICFILES_STORAGE
DEFAULT_FILE_STORAGE = global_settings.DEFAULT_FILE_STORAGE
