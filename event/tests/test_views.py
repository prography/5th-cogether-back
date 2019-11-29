from model_bakery import baker

from cogether.tests.testcase import TestCase


class TestBoardViews(TestCase):
    def setUp(self):
        pass

    def test_event_list(self):
        response = self.get_check_200('event:event-list')
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 0)
        self.assertEqual(json_resp['results'], [])

        # create event
        event = baker.make(
            'event.DevEvent',
            title='event1'
        )
        response = self.get_check_200('event:event-list')
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], event.id)

    def test_event_list_when_category_does_not_exist(self):
        pass
