import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:  # If there is session timezone, get it
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()   # If there is no session timezone, use server time
        return self.get_response(request)
