import pytz
from django.utils import timezone


def timezone_context(request):
    current_time = timezone.now()
    current_hour = current_time.astimezone(timezone.get_current_timezone()).hour
    return {
        'current_time': timezone.now(),
        'current_hour': current_hour,
        'timezones': pytz.common_timezones,
        'TIME_ZONE': timezone.get_current_timezone_name()
    }
