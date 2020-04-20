from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DataActionItemModelWrapper(ModelWrapper):

    model = 'edc_data_manager.dataactionitem'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'data_manager_listboard_url')
