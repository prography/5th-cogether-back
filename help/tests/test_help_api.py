import os

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from help.models import HelpCenter, HelpInfo, FREQ, MY, HELP, UPDATEREQUEST, CREATEREQUEST
from help.serializers import HelpCenterSerializer, HelpInfoSerializer

HELP_INFO_URL = reverse('help:info-list')
HELP_FREQ_LIST_URL = reverse('help:freq-list')
HELP_MY_LIST_URL = reverse('help:my-list')


def freq_detail_url(help_id):
    return reverse('help:freq-detail', args=[help_id])


def my_detail_url(help_id):
    return reverse('help:my-detail', args=[help_id])


def sample_question(user, **param):
    defaults = {
        "title": "default title",
        "contents": "default contents",
        "type": MY,

        "answered_by": "default admin",
        "answer": "default answer"
    }
    # print('\n', defaults, '\n')
    defaults.update(param)

    return HelpCenter.objects.create(user=user, **defaults)


def sample_user():
    user = get_user_model().objects.create_user(
        'testhelpfreq@sisi.com',
        'testpass'
    )
    return user


class PublicHelpAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_info_access(self):
        res = self.client.get(HELP_INFO_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_info_list_access(self):
        test_data = ["안녕하세요", "Cogether 입니다."]
        HelpInfo.objects.create(contents=test_data[0])
        HelpInfo.objects.create(contents=test_data[1])

        res = self.client.get(HELP_INFO_URL)  # , format='json')

        info_list = HelpInfo.objects.all().order_by('id')
        serializer = HelpInfoSerializer(info_list, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print('\n', res.data, '\n')
        self.assertEqual(res.data, serializer.data)

    def test_freq_list_access(self):
        test_user = sample_user()
        sample_question(user=test_user, type=MY)
        freq_question = sample_question(user=test_user, type=FREQ)

        res = self.client.get(HELP_FREQ_LIST_URL)

        serializer = HelpCenterSerializer(freq_question)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer.data, res.data)

    def test_freq_detail_access(self):
        test_user = sample_user()
        sample_question(user=test_user, type=MY)
        freq_question = sample_question(user=test_user, type=FREQ)

        url = freq_detail_url(freq_question.id)
        res = self.client.get(url)

        serializer = HelpCenterSerializer(freq_question)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_my_list_access(self):  how to raise 401 error
    #     #  help.tests.test_help_api.PublicHelpAPITests.test_my_list_access
    #     res = self.client.get(HELP_MY_LIST_URL)
    #
    #     self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    #     # status.302


class PrivateHelpAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'sisitest@sisi.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_my_question_list(self):
        sample_question(user=self.user)
        sample_question(user=self.user)

        res = self.client.get(HELP_MY_LIST_URL)

        my_questions = HelpCenter.objects.all()
        serializer = HelpCenterSerializer(my_questions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_my_question_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'other@sisi.com',
            'password'
        )
        sample_question(user=self.user)
        sample_question(user=user2)

        res = self.client.get(HELP_MY_LIST_URL)

        questions = HelpCenter.objects.filter(user=self.user)
        serializer = HelpCenterSerializer(questions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_my_question_detail(self):
        # help.tests.test_help_api.PrivateHelpAPITests.test_my_question_detail
        question = sample_question(user=self.user)

        url = my_detail_url(question.id)
        res = self.client.get(url)

        serializer = HelpCenterSerializer(question)
        self.assertEqual(res.data, serializer.data)

    def test_create_my_question_personal(self):
        payload = {
            "title": "default title",
            "contents": "default contents",
            "source": HELP
        }
        res = self.client.post(HELP_MY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        question = HelpCenter.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(question, key))

    def test_create_my_question_request_creating(self):
        payload = {
            "title": "default title",
            "contents": "default contents",
            "source": CREATEREQUEST
        }
        res = self.client.post(HELP_MY_LIST_URL, payload)

        res = self.client.post(HELP_MY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        question = HelpCenter.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(question, key))

    def test_create_my_question_request_updating(self):
        payload = {
            "title": "default title",
            "contents": "default contents",
            "source": UPDATEREQUEST
        }
        res = self.client.post(HELP_MY_LIST_URL, payload)

        res = self.client.post(HELP_MY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        question = HelpCenter.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(question, key))

    def test_partial_update_my_question(self):
        question = sample_question(user=self.user)

        payload = {"title": "updated title"}
        url = my_detail_url(question.id)
        self.client.patch(url, payload)

        question.refresh_from_db()

        self.assertEqual(question.title, payload['title'])

    def test_full_update_my_question(self):
        question = sample_question(user=self.user)

        payload = {
            'title': "updated title",
            'contents': "updated contents"
        }

        url = my_detail_url(question.id)
        self.client.put(url, payload)

        question.refresh_from_db()

        self.assertEqual(question.title, payload['title'])
        self.assertEqual(question.contents, payload['contents'])

    def test_delete_my_question(self):
        # help.tests.test_help_api.PrivateHelpAPITests.test_delete_my_question
        question = sample_question(user=self.user)

        url = my_detail_url(question.id)
        res = self.client.delete(url)

        print('\n', type(res), '\n')

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
