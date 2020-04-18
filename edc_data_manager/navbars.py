from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'edc_data_manager' else False

data_manager = Navbar(name='data_manager')

data_manager.append_item(
    NavbarItem(
        name='data_manager',
        title='Data Manager',
        label='EDC Data Manager',
        fa_icon='fa fa-data-manager',
        url_name=settings.DASHBOARD_URL_NAMES[
            'data_manager_listboard_url'],
        no_url_namespace=no_url_namespace))


site_navbars.register(data_manager)
