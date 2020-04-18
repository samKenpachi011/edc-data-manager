from django.conf import settings
from edc_model_wrapper import ModelWrapper


class DataActionItemModelWrapper(ModelWrapper):

    model = 'edc_data_manager.dataactionitem'
    next_url_attrs = ['subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'data_manager_listboard_url')

    @property
    def file_url(self):
        """Return the file url.
        """
        return self.object.document.url

    @property
    def files_generation_time(self):
        """return file generation time in minutes
        """
        download_time = self.object.downnload_time
        if download_time:
            return round(float(self.object.downnload_time) / 60.0, 2)
        return None
