from django.test import TestCase

from .models import DataActionItem


class TestDataActionItem(TestCase):

    def setUp(self):
        self.options = {
            'subject_identifier': '123124',
            'comment': 'This participant need to take PBMC for storage'}

    def test_data_Action_item(self):
        """Test creation of a data action item.
        """
        DataActionItem.objects.create(
            **self.options)
        data_action_item = DataActionItem.objects.all()
        self.assertEqual(data_action_item.count(), 1)
