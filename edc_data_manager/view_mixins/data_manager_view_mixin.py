from django.contrib import messages
from django.views.generic.base import ContextMixin

from edc_constants.constants import OPEN

from ..models import DataActionItem
from ..model_wrappers import DataActionItemModelWrapper


class DataActionItemsViewMixin(ContextMixin):

    data_action_item_template = 'edc_data_manager/data_manager.html'

    @property
    def data_action_item(self):
        """Returns a wrapped saved or unsaved consent version.
        """
        model_obj = DataActionItem(subject_identifier=self.subject_identifier)
        return DataActionItemModelWrapper(model_obj=model_obj)

    def data_action_items(self):
        """Return a list of action items.
        """
        wrapped_data_action_items = []
        status = [OPEN, 'stalled', 'resolved']
        data_action_items = DataActionItem.objects.filter(
            subject_identifier=self.subject_identifier,
            status__in=status).order_by('issue_number')
        for data_action_item in data_action_items:
            wrapped_data_action_items.append(data_action_item)
        return wrapped_data_action_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status = [OPEN, 'stalled', 'resolved']
        data_action_items = DataActionItem.objects.filter(
            subject_identifier=self.subject_identifier,
            status__in=status).order_by('issue_number')
        msg = ''
        for data_action_item in data_action_items:
            msg = (f'Issue {data_action_item.issue_number}. Pending action'
                   f' created by {data_action_item.user_created}. '
                   f'{data_action_item.subject} Assigned to '
                   f'{data_action_item.assigned}')
            messages.add_message(
                self.request, messages.ERROR, msg)

        context.update(
            data_action_item_template=self.data_action_item_template,
            data_action_item_add_url=self.data_action_item.href,
            data_action_items=self.data_action_items)
        return context
