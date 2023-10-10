from django.conf import settings
from edc_model_wrapper import ModelWrapper
from edc_base.utils import get_utcnow


class DataActionItemModelWrapper(ModelWrapper):

    model = 'edc_data_manager.dataactionitem'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')

    @property
    def age(self):
        """Returns the ticket age.
        """
        delta = get_utcnow().date() - self.object.created.date()
        return delta.days
