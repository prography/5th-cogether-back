"""
MEETUP API: https://www.meetup.com/ko-KR/meetup_api/
"""
from event.models import Category, Photo, DevEvent
import requests
from datetime import datetime, timedelta

from django.core.files.base import ContentFile


korea_meetup_dev_group = {
    'GDG-Seoul', 'awskrug', 'HashedLounge', 'seoul-tech-society',
    'IBM-developerWorks-Meetup', 'KryptoSeoul', 'codeseoul',
    'Seoul-Cloud-Foundry-Meetup', 'Hyperledger-Korea', 'OracleDeveloperKR',
    'GDG-Cloud-Korea', 'Korea-Ravencoin', 'GDG-WebTech', 'golangskynet',
    'Hongdae-Machine-Learning-Study', 'Seoul-Startup-Founders-101',
    'theslowtech', 'BlockchainROK', 'Cloud-Native-Computing-Seoul',
    'Internet-of-Things-Korea-Meetup', 'react-native-seoul', 'graphdatabase',
    'Cosmos-Seoul', 'Korea-Blockchain-Hub', 'KOREASLUG', 'Software-QA'
}

MIMETYPE = {
    "image/bmp": '.bmp',
    'image/jpeg': '.jpg',
    'image/png': '.png',
}


def save_new_events_from_meetup_dev_group(korea_meetup_dev_group):
    """meetup api를 이용해 새로운 개발 행사를 데이터베이스에 저장합니다.
    
    Arguments:
        korea_meetup_dev_group {dict} -- [meetup 국내 개발 그룹 이름]
    """
    for group in korea_meetup_dev_group:
        url = 'https://api.meetup.com/%s/events?&sign=true&photo-host=public&page=50&fields=group_key_photo,featured_photo' % (
            group)
        response = requests.get(url)
        response_json = response.json()
        for event in range(len(response_json)):
            category_instance = Category.objects.get(name='conference')

            photo_instance = get_photo_instance(response_json)

            event_dict = set_devevent_field_to_dict(response_json)
            event_dict['photo'] = photo_instance
            event_dict['category'] = category_instance

            if not_exists_event(event_dict['original_identity']):
                meetup_crawling_event = DevEvent(**event_dict)
                meetup_crawling_event.save()


def get_photo_instance(response_json):
    """사진을 데이터베이스에 저장하고 그 인스턴스를 반환합니다.
    
    이벤트의 대표 사진을 저장하고 그것이 없을 경우 그룹의 대표 사진을 저장합니다.

    Arguments:
        response_json {json} -- [meetup api로부터 받은 응답]
    
    Returns:
        [Photo model] -- [해당 이벤트의 사진]
    """
    photo_url = get_photo_url(response_json[0].get(
        'group'), response_json[0].get('featured_photo'))

    if Photo.objects.filter(original_url=photo_url).exists():
        return Photo.objects.get(original_url=photo_url)

    photo = requests.get(photo_url)
    image_extension = MIMETYPE[photo.headers['Content-Type']]
    photo_instance = Photo.objects.create(original_url=photo_url)
    photo_instance.photo.save(
        'image' + image_extension, ContentFile(photo.content), save=True)
    return photo_instance


def set_devevent_field_to_dict(response_json):
    """meetup api로부터 받은 데이터를 DevEvent 필드에 맞게 dict형으로 변경합니다.
    
    Arguments:
        response_json {json} -- [meetup api로부터 받은 응답]
    
    Returns:
        [dict] -- [DevEvent 필드를 key로 가진 dict]
    """
    event_dict = dict()

    start_at, end_at = get_start_and_end_time(response_json[0])
    venue = get_venue(response_json[0].get('venue'))
    photo_url = get_photo_url(response_json[0].get(
        'group'), response_json[0].get('featured_photo'))

    event_dict['original_identity'] = response_json[0]['id']
    event_dict['title'] = response_json[0]['name']
    event_dict['host'] = response_json[0]['group']['name']
    event_dict['content'] = response_json[0]['description']

    event_dict['external_link'] = response_json[0]['link']
    event_dict['location'] = venue
    event_dict['source'] = 'meetup_crawling'
    event_dict['status'] = 'development'

    event_dict['start_at'] = start_at
    event_dict['end_at'] = end_at
    return event_dict


def not_exists_event(original_identity):
    """존재하지 않는 이벤트인지 확인합니다.
    
    Arguments:
        original_identity {int} -- [meetup의 event id]
    
    Returns:
        [bool] -- [이벤트가 존재하면 False를 반환]
    """
    return (not DevEvent.objects.filter(source='meetup_crawling', original_identity=original_identity).exists())


def get_start_and_end_time(response_json):
    """이벤트 시작시간과 종료시간을 구합니다.
    
    Arguments:
        response_json {json} -- [meetup api로부터 받은 응답]
    
    Returns:
        [datetime, datetime] -- [이벤트 시작시간, 이벤트 종료시간]
    """
    start_at = datetime.fromisoformat(
        response_json['local_date'] + ' ' + response_json['local_time'])
    end_at = start_at + \
        timedelta(milliseconds=response_json['duration'])
    return start_at, end_at


def get_venue(venue_json):
    """이벤트 장소를 구합니다.
    
    Arguments:
        venue_json {json} -- [meetup api로부터 받은 응답]
    
    Returns:
        [str] -- [이벤트 장소]
    """
    location = ""
    if venue_json is None:
        return location
    else:
        if venue_json.get('city') is not None:
            location += venue_json.get('city')
        if venue_json.get('address_1') is not None:
            location += ' ' + venue_json.get('address_1')
        if venue_json.get('address_2') is not None:
            location += ' ' + venue_json.get('address_2')
        if venue_json.get('address_3') is not None:
            location += ' ' + venue_json.get('address_3')
        if venue_json.get('name') is not None:
            location += ' ' + venue_json.get('name')
        return location


def get_photo_url(group_photo, featured_photo):
    """이벤트의 사진이 저장되어있는 외부 서비스의 url을 구합니다.

    해당 이벤트의 대표 사진의 url을 구합니다. 이벤트 대표 사진 url이 없다면, 그룹의 대표 사진 url을 구합니다.
    
    Arguments:
        group_photo {json} -- [그룹의 사진 정보가 저장된 json]
        featured_photo {json} -- [이벤트의 사진 정보가 저장된 json]
    
    Returns:
        [str] -- [이벤트 대표 사진]
    """
    if featured_photo is None:
        return group_photo.get('key_photo').get('photo_link')
    return featured_photo.get('photo_link')


if __name__ == '__main__':
    save_new_events_from_meetup_dev_group(korea_meetup_dev_group)
