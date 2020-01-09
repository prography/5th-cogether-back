"""
FESTA API: https://festa.io/api/v1/events?page=1&pageSize=90&order=startDate&excludeExternalEvents=false
"""
import os
import sys
sys.path.append('..')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cogether.settings.dev")

import django
django.setup()


from event.models import Category, Photo, DevEvent
import requests
from datetime import datetime, timedelta

from django.core.files.base import ContentFile


def save_new_events_from_festa_dev_group():
    """festa api를 이용해 새로운 개발 행사를 데이터베이스에 저장합니다.
    
    """
    url = 'https://festa.io/api/v1/events?page=1&pageSize=50&order=startDate&excludeExternalEvents=false'
    response = requests.get(url)
    response_json = response.json()['rows']

    for event in response_json:
        event_dict = set_devevent_field_to_dict(event)

        category_instance = Category.objects.get(name='conference')
        event_dict['category'] = category_instance

        photo_instance = get_photo_instance(event)
        event_dict['photo'] = photo_instance

        if not_exists_event(event_dict['original_identity']):
            festa_crawling_event = DevEvent(**event_dict)
            festa_crawling_event.save()


def get_photo_instance(response_json):
    """사진을 데이터베이스에 저장하고 그 인스턴스를 반환합니다.
    
    이벤트의 대표 사진을 저장하고 그것이 없을 경우 그룹의 대표 사진을 저장합니다.

    Arguments:
        response_json {json} -- [festa api로부터 받은 응답]
    
    Returns:
        [Photo model] -- [해당 이벤트의 사진]
    """
    photo_url = get_photo_url(
        response_json['hostOrganization'].get('profileImage'),
        response_json['hostOrganization'].get('bannerImage'),
        response_json['metadata'].get('coverImage'))

    if Photo.objects.filter(original_url=photo_url).exists():
        return Photo.objects.get(original_url=photo_url)

    photo = requests.get(photo_url)
    image_extension = photo_url.split(".")[-1]
    photo_instance = Photo.objects.create(original_url=photo_url)
    photo_instance.photo.save(
        'image' + image_extension, ContentFile(photo.content), save=True)
    return photo_instance


def set_devevent_field_to_dict(response_json):
    """festa api로부터 받은 데이터를 DevEvent 필드에 맞게 dict형으로 변경합니다.
    
    Arguments:
        response_json {json} -- [festa api로부터 받은 응답]
    
    Returns:
        [dict] -- [DevEvent 필드를 key로 가진 dict]
    """
    event_dict = dict()

    start_at, end_at = get_start_and_end_time(response_json)
    venue = get_venue(response_json['location'])
    external_link = get_event_link(response_json)

    event_dict['original_identity'] = response_json['eventId']
    event_dict['title'] = response_json['name']
    event_dict['host'] = response_json['hostOrganization']['name']
    event_dict['content'] = response_json['metadata']['contents']

    event_dict['external_link'] = external_link
    event_dict['location'] = venue
    event_dict['source'] = 'festa_crawling'
    event_dict['status'] = 'unclassified_events'

    event_dict['start_at'] = start_at
    event_dict['end_at'] = end_at
    return event_dict


def not_exists_event(original_identity):
    """존재하지 않는 이벤트인지 확인합니다.
    
    Arguments:
        original_identity {int} -- [festa event id]
    
    Returns:
        [bool] -- [이벤트가 존재하면 False를 반환]
    """
    return (not DevEvent.objects.filter(source='festa_crawling', original_identity=original_identity).exists())


def get_start_and_end_time(response_json):
    """이벤트 시작시간과 종료시간을 구합니다.
    festa에서는 UTC 시간을 사용하므로 한국 시간으로 바꾸기 위해 9시간을 더합니다.
    
    Arguments:
        response_json {json} -- [festa api로부터 받은 응답]
    
    Returns:
        [datetime, datetime] -- [이벤트 시작시간, 이벤트 종료시간]
    """
    start_at = datetime.fromisoformat(response_json['startDate'][:-1]) + timedelta(hours=9)
    end_at = datetime.fromisoformat(response_json['endDate'][:-1]) + timedelta(hours=9)
    return start_at, end_at


def get_venue(venue_json):
    """이벤트 장소를 구합니다.
    
    Arguments:
        venue_json {json} -- [festa api로부터 받은 응답]
    
    Returns:
        [str] -- [이벤트 장소]
    """
    location = ""
    if venue_json is None:
        return location
    else:
        if venue_json.get('address') is not None:
            location += venue_json.get('address')
        if venue_json.get('name') is not None:
            location += ' ' + venue_json.get('name')
        return location


def get_event_link(response_json):
    if response_json['external'] == 'true':
        return response_json['externalLink']    
    return 'https://festa.io/events/{}'.format(response_json['eventId'])


def get_photo_url(host_profile_url, host_banner_url, event_photo_url):
    """이벤트 사진의 url을 구합니다.

    해당 이벤트의 대표 사진의 url을 구합니다.
    이벤트 대표 사진 url이 없다면, 호스트의 대표 사진 url을 구합니다.
    호스트의 대표 사진이 없다면 호스트의 프로필 사진 url을 구합니다.
    
    Arguments:
        host_profile_url {str} -- [호스트의 프로필 사진 url]
        host_banner_url {str} -- [호스트의 대표 사진 url]
        event_photo_url {str} -- [이벤트의 대표 사진 url]
    Returns:
        [str] -- [이벤트 대표 사진]
    """
    if event_photo_url is not None:
        return event_photo_url
    if host_banner_url is not None:
        return host_banner_url
    return host_profile_url


if __name__ == '__main__':
    save_new_events_from_festa_dev_group()
