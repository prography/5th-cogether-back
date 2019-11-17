from cogether.tests.testcase import TestCase
from model_mommy.mommy import make as mm

from event.models import Event, Category


class TestBoardVies(TestCase):
    def setUp(self):
        self.category = mm(Category, name='conference')
        self.event = mm(Event, title='event1', category=self.category)
        self.event_without_category = mm(Event, title='event1')

    def test_event_list(self):
        pass

    def test_event_list_when_category_does_not_exist(self):
        self.get_check_200('board:board-list')
