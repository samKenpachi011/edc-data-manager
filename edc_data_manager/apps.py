from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    """
    extra_assignee_choices:
    {'td_clinic': [
    ('choice_value', 'choice_displayed_value'), [list_of_emails]],}
    """
    name = 'edc_data_manager'
    verbose_name = "EDC Data Manager"
    admin_site_name = 'edc_data_manager_admin'
    extra_assignee_choices = ()
    identifier_pattern = None
    assignable_users_group = 'assignable users'
    assianable_suers_notofication = False
    email_issue_notification = False

    def ready(self):
        from .signals import data_action_item_on_post_save
