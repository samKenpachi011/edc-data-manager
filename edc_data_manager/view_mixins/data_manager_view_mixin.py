from django.views.generic.base import ContextMixin

from ..models import DataActionItem


class DataActionItemsViewMixin(ContextMixin):

    data_action_item_template = None

    def data_action_items(self):
        """Return a list of action items.
        """
        data_action_items = DataActionItem.objects.filter(
            subject_identifier=self.subject_identifier)
        return data_action_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            data_action_item_template=self.data_action_item_template,
            data_action_item_add_url=DataActionItem().get_absolute_url())
        return context

    