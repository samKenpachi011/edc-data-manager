from django.conf import settings
from edc_model_wrapper import ModelWrapper

from edc_base.utils import get_utcnow


class DataActionItemModelWrapper(ModelWrapper):

    model = 'edc_data_manager.dataactionitem'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')

    @property
    def issue_age(self):
        """Return how many days an issues has been existing unresolved.
        """
        date_diff = get_utcnow() - self.object.created
        return date_diff.days
 
    @property
    def date_created(self):
        """Reurns the date of creation.
        """
        return self.object.created.date().strftime("%d %b %Y")