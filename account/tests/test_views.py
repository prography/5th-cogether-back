from model_bakery import baker

from cogether.tests.testcase import TestCase


class TestAccountViews(TestCase):
    def setUp(self):
        self.user1 = baker.make(
            'account.MyUser',
            username='user1',
            password='password'
        )

    def test_account_list(self):
        resp = self.get_check_200('account:account-list')

        self.assertEqual(resp.json()['count'], 1)
        self.assertEqual(resp.json()['results'][0]['id'], self.user1.id)

    def test_create_account(self):
        pass
