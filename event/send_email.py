import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from event.models import DevEvent

MyUser = get_user_model()


def send_event_emails_to_subscribers():
    today = datetime.datetime.today()
    created_last_week_event = DevEvent.objects.filter(
        created_at__range=(today + datetime.timedelta(days=-7), today))
    start_this_week_event = DevEvent.objects.filter(
        start_at__range=(today, today + datetime.timedelta(days=7)))

    subject = 'Co.gether에서 국내 개발 행사 일정을 알려드립니다!'
    html_message = render_to_string('event/cogether_subscribe_email.html', {
        'created_last_week_event': created_last_week_event,
        'start_this_week_event': start_this_week_event
    })
    plain_message = strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = MyUser.objects.filter(is_active=True).filter(is_superuser=False)

    for user in to:
        mail.send_mail(subject, plain_message, from_email,
                       [user.username], html_message=html_message)
    return len(to)
