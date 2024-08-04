import pytz
from django.utils import timezone


def timezone_context(request):
    return {
        'current_time': timezone.now(),
        'timezones': pytz.common_timezones,
        'TIME_ZONE': timezone.get_current_timezone_name()
    }
