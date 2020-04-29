from edc_navbar import NavbarItem, site_navbars, Navbar

data_manager = Navbar(name='data_manager')

data_manager.append_item(
    NavbarItem(name='edc_data_manager',
               label='Edc Data Manager',
               fa_icon='fa-cogs',
               url_name='edc_data_manager:home_url'))

site_navbars.register(data_manager)
