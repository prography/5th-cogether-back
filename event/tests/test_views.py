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


class TestDevEventSearchByCategory(TestCase):
    """ Test class for DevEvent model search by category """
    def setup(self):
        pass

    def test_no_events(self):
        self.category = baker.make('event.Category')

        response = self.get_check_200(
            'event:event-list', data={'category': self.category.name})
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 0)

    def test_no_match_events(self):
        self.category = baker.make('event.Category')
        self.other_category = baker.make(
            'event.Category', name=self.category.name+'t')
        self.event = baker.make('event.DevEvent', category=self.category)

        response = self.get_check_200(
            'event:event-list', data={'category': self.other_category.name})
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 0)

    def test_one_match_events(self):
        self.category = baker.make('event.Category')
        self.event = baker.make('event.DevEvent', category=self.category)

        response = self.get_check_200(
            'event:event-list', data={'category': self.category.name})
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], self.event.id)
        self.assertEqual(json_resp['results'][0]
                         ['category']['name'], self.category.name)

    def test_no_match_and_match_events(self):
        self.category = baker.make('event.Category')
        self.other_category = baker.make(
            'event.Category', name=self.category.name+'something')
        self.event = baker.make('event.DevEvent', category=self.category)
        self.no_match_event = baker.make(
            'event.DevEvent', category=self.other_category)

        response = self.get_check_200(
            'event:event-list', data={'category': self.category.name})
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], self.event.id)
        self.assertEqual(json_resp['results'][0]
                         ['category']['name'], self.category.name)

    def test_many_match_events(self):
        self.category = baker.make('event.Category')
        self.many_events = baker.make(
            'event.DevEvent', category=self.category, _quantity=5)

        response = self.get_check_200(
            'event:event-list', data={'category': self.category.name})
        json_resp = response.json()

        many_events_id = [event.id for event in self.many_events]

        for result in json_resp['results']:
            self.assertEqual(result['id'] in many_events_id, True)


class TestDevEventSearchViews(TestCase):
    """ Test module for DevEvent model """

    def setUp(self):
        pass

    def test_no_events(self):
        pass

    def test_no_match_events(self):
        pass

    def test_one_match_event(self):
        pass

    def test_no_match_and_match_events(self):
        pass

    def test_many_match_events(self):
        pass
    