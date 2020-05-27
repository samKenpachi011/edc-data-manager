from django.apps import apps as django_apps
from django.urls.conf import path

from edc_dashboard import UrlConfig

from .admin_site import edc_data_manager_admin
from .views import HomeView, ListBoardView

app_name = 'edc_data_manager'
app_config = django_apps.get_app_config('edc_data_manager')

urlpatterns = [
    path('admin/', edc_data_manager_admin.urls),
    path('', HomeView.as_view(), name='home_url'),
]

data_manager_listboard_url_config = UrlConfig(
    url_name='data_manager_listboard_url',
    view_class=ListBoardView,
    label='data_manager_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=app_config.identifier_pattern)

urlpatterns += data_manager_listboard_url_config.listboard_urls
