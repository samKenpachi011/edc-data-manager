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
    # extra_assignee_choices = ()
    identifier_pattern = None
    assignable_users_group = 'assignable users'
    assianable_users_note = False
    email_issue_notification = True
    extra_assignee_choices = {
        'gabs_clinic': [
            ('gabs_clinic', 'AZD Gababorone Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'maun_clinic': [
            ('maun_clinic', 'AZD Maun Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'serowe_clinic': [
            ('serowe_clinic', 'AZD Serowe Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'gheto_clinic': [
            ('gheto_clinic', 'AZD Francistown Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'sphikwe_clinic': [
            ('sphikwe_clinic', 'AZD Selibe Phikwe Clinic'),
            ['bhp.se.dmc@gmail.com']],
        'se_dmc': [
            ('se_dmc', 'SE & Data Management'),
            ['adiphoko@bhp.org.bw', 'ckgathi@bhp.org.bw', 'imosweu@bhp.org.bw',
             'mmotlhanka@bhp.org.bw', 'mchawawa@bhp.org.bw', 'nmunatsi@bhp.org.bw']]}

    def ready(self):
        from .signals import data_action_item_on_post_save
