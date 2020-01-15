import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from event.models import DevEvent


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
