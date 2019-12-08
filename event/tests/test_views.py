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

    def test_unmatch_events(self):
        self.category = baker.make('event.Category')
        self.other_category = baker.make(
            'event.Category', name=self.category.name[:30] + 'something')
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

    def test_unmatch_and_match_events(self):
        self.category = baker.make('event.Category')
        self.other_category = baker.make(
            'event.Category', name=self.category.name[:30] + 'something')
        self.event = baker.make('event.DevEvent', category=self.category)
        self.unmatch_event = baker.make(
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


class TestDevEventSearchByTitle(TestCase):
    """ Test module for DevEvent model """

    def setUp(self):
        pass

    def test_no_events(self):
        self.title = '프론트'

        response = self.get_check_200(
            'event:event-list', data={'title': self.title}
        )
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 0)

    def test_unmatch_events(self):
        self.title = '프론트'
        self.other_title = '백엔드'
        self.event = baker.make('event.DevEvent', title=self.other_title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title}
        )
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 0)

    def test_one_match_event(self):
        self.title = '프론트'
        self.event = baker.make('event.DevEvent', title=self.title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title})
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], self.event.id)
        self.assertEqual(json_resp['results'][0]['title'], self.title)

    def test_one_match_with_sub_title_event(self):
        self.title = '프론트엔드'
        self.sub_title = '프론트'
        self.event = baker.make('event.DevEvent', title=self.title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.sub_title})
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], self.event.id)
        self.assertEqual(json_resp['results'][0]['title'], self.title)

    def test_one_match_with_delimiters(self):
        self.title = '프론트'
        self.title_with_delimiters = '프론.트'
        self.event = baker.make('event.DevEvent', title=self.title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title_with_delimiters})
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 0)

    def test_one_match_with_space(self):
        self.title = '프론트'
        self.title_with_space = '프 론트'
        self.event = baker.make('event.DevEvent', title=self.title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title_with_space})
        json_resp = response.json()
        self.assertEqual(json_resp['count'], 0)

    def test_unmatch_and_match_events(self):
        self.title = '프론트'
        self.unmatch_title = '백엔드'
        self.event = baker.make('event.DevEvent', title=self.title)
        self.unmatch_event = baker.make(
            'event.DevEvent', title=self.unmatch_title)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title})
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 1)
        self.assertEqual(json_resp['results'][0]['id'], self.event.id)
        self.assertEqual(json_resp['results'][0]['title'], self.title)

    def test_many_match_events(self):
        self.title = '프론트'
        self.many_events = baker.make(
            'event.DevEvent', title=self.title, _quantity=5)

        response = self.get_check_200(
            'event:event-list', data={'title': self.title})
        json_resp = response.json()

        many_events_id = [event.id for event in self.many_events]

        for result in json_resp['results']:
            self.assertEqual(result['id'] in many_events_id, True)


class TestDevEventSearchByAllParameter(TestCase):
    def setup(self):
        pass

    def test_match_category_and_match_title(self):
        self.category = baker.make('event.Category')
        self.unmatch_category = baker.make('event.Category', name=self.category.name[:30] + 'something')
        self.title = '프론트'
        self.event = baker.make('event.DevEvent', title=self.title, category=self.category, _quantity=5)
        self.unmatch_event = baker.make('event.DevEvent', category=self.unmatch_category, _quantity=5)
        event_id = [event.id for event in self.event]

        response = self.get_check_200('event:event-list', data={'title': self.title, 'category': self.category.name})
        json_resp = response.json()

        self.assertEqual(json_resp['count'], 5)
        for result in json_resp['results']:
            self.assertEqual(result['id'] in event_id ,True)
