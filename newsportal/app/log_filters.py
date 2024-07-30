from django.conf import settings
import logging


class RequireDebugFalse(logging.Filter):    # Custom logging filter to disable console logging when DEBUG = False
    def filter(self, record):
        return not settings.DEBUG
