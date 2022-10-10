from datetime import date
from django.utils.timezone import now
import re


def calculate_age(dob):
    today = date.today()
    try:
        age = (today.year - dob.year) \
              - ((today.month, today.day) < (dob.month, dob.day))
    except ValueError:
        age = 0
    return age


def is_mobile(request):
    """Return True if the request comes from a mobile device."""

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False
