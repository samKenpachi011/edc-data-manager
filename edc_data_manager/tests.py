from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag

from .models import DataActionItem


class TestDataActionItem(TestCase):

    def setUp(self):
        self.assigned_user = User.objects.create_user(
            username='testuser', password='12345')
        self.user_created = User.objects.create_user(
            username='testuser2', password='12345')
        self.options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage',
            'assigned': self.assigned_user.username,
            'user_created': self.user_created.username}

    def test_data_action_item(self):
        """Test creation of a data action item.
        """
        DataActionItem.objects.create(
            **self.options)
        data_action_item = DataActionItem.objects.all()

        self.assertEqual(data_action_item.count(), 1)

    def test_action_item_sequnce_numbering(self):
        """Test creation of a data action item issue number increments sequentially.
        """
        count = 1
        while count < 4:
            data_action_item = DataActionItem.objects.create(
                **self.options)
            self.assertEqual(data_action_item.issue_number, count)
            count += 1

    @tag('vv')
    def test_user_assigned(self):
        """Test that an issue can not be created if user assigned does not exists.
        """
        options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage',
            'user_created': self.user_created.username}
        with self.assertRaises(ObjectDoesNotExist) as error:
            DataActionItem.objects.create(**options)
        self.assertEqual(
            error.exception.args[0],
            'User does not exist')

    def test_user_assigning(self):
        """Test that an issue can not be created if the user
        assigning does not exists as a django user.
        """
        options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage',
            'assigned': self.assigned_user.username}
        with self.assertRaises(ObjectDoesNotExist) as error:
            DataActionItem.objects.create(**options)
        self.assertEqual(
            error.exception.args[0],
            'The user that created the data issue 1 does not exist.')
