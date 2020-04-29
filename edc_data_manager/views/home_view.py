from django.views.generic import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin


class HomeView(EdcBaseViewMixin, TemplateView):

    template_name = 'edc_data_manager/home.html'
