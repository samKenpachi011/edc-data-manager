from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'edc_data_manager'
    verbose_name = "EDC Data Manager"
    admin_site_name = 'edc_data_manager_admin'

    def ready(self):
        from .signals import data_action_item_on_post_save
