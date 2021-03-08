from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

edc_data_manager = Navbar(name='edc_data_manager')
no_url_namespace = True if settings.APP_NAME == 'edc_data_manager' else False

edc_data_manager.append_item(
    NavbarItem(name='edc_data_manager',
               label='Data Manager Usage',
               fa_icon='fa-cogs',
               url_name='edc_data_manager:home_url'))

edc_data_manager.append_item(
    NavbarItem(
        name='data_manager',
        title='EDC Data Manager',
        label='EDC Data Manager',
        fa_icon='fa fa-file-export',
        url_name=settings.DASHBOARD_URL_NAMES[
            'data_manager_listboard_url'],
        no_url_namespace=no_url_namespace))

edc_data_manager.append_item(
    NavbarItem(name='data_manager_admin',
               label='Data Manager Admin',
               fa_icon='fa-cogs',
               url_name='edc_data_manager:admin_url'))

site_navbars.register(edc_data_manager)
