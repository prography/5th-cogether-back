import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core import mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from event.models import DevEvent


def test_email():
    today = datetime.datetime.today()
    created_last_week_event = DevEvent.objects.filter(
        created_at__range=(today + datetime.timedelta(days=-7), today))
    start_this_week_event = DevEvent.objects.filter(
        start_at__range=(today, today + datetime.timedelta(days=7)))

    subject = 'Subject'
    html_message = render_to_string(
        'event/cogether_subscribe_email.html',
        {'created_last_week_event': created_last_week_event,
         'start_this_week_event': start_this_week_event})
    plain_message = strip_tags(html_message)
    from_email = 'cogether4@gmail.com'
    # TODO: to에 subscribe 필드가 True인 일반 유저(admin 제외, is_active가 True)의 목록을 저장하기.
    to = ['wlckd90@gmail.com', 'wlckdzlffj90@naver.com']

    mail.send_mail(subject, plain_message, from_email,
                   to, html_message=html_message)


def send_emails():
    users = get_user_model().objects.filter(subscribe=True)

    user_email_list = []
    # 모든 사용자
    for u in users:
        user_email_list.append(str(u))

    now = datetime.datetime.now()
    yesterday = now + datetime.timedelta(days=-1)
    new_events = DevEvent.objects.filter(created_at__range=(yesterday, now))

    if len(new_events) == 0:
        print('새로운 이벤트가 없습니다')
        return
    else:
        titles = []
        for e in new_events:
            titles.append(e.title + '\n')
        titles_string = ''.join(titles)
        print('새로 등록된 이벤트를 메일로 알립니다.', titles_string)

    cogether_url = "https://cogether.kr/conference/"
    html_content = '<h2>안녕하세요 오늘 등록된 이벤트 알립니다!</h2>'
    html_content += '<table ><thead><tr>'
    html_content += '<th>Title</th>'
    html_content += '<th>Host</th>'
    html_content += '<th>Date</th>'
    html_content += '</tr></thead><tbody>'

    tmp = ''
    for e in new_events:
        tmp = '<tr >'
        #
        tmp += '<td style="width:55%;">' + '<a style="text-decoration:none;" href="' + cogether_url + str(
            e.id) + '/">' + e.title + '</a>' + '</td>'
        #
        tmp += '<td style="font-size:85%;width:25%;">' + e.host + '</td>'
        start_date = e.start_at.strftime('%m월 %d일 %A %H시 %M분'.encode('unicode-escape').decode()).encode().decode(
            'unicode-escape')
        end_date = e.end_at.strftime('%m월 %d일 %A %H시 %M분'.encode('unicode-escape').decode()).encode().decode(
            'unicode-escape')
        #
        tmp += f'<td style="font-size:80%;width:25%;margin:50%;">{start_date + " <br/>~ " + end_date}</td>'
        tmp += '</tr>'

        html_content += tmp
    html_content += '</tbody><tfoot><tr><td colspan="5"><br/>Cogether를 이용해주셔서 감사합니다!</td></tr></tfoot></table>'

    subject, from_email, to_emails = 'hello', settings.EMAIL_HOST_USER, user_email_list
    text_content = titles_string

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
