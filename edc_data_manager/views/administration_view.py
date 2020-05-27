from django.views.generic import TemplateView
from edc_base.view_mixins import AdministrationViewMixin
from edc_base.view_mixins import EdcBaseViewMixin

from ..view_mixins import UserDetailsCheckViewMixin


class AdministrationView(UserDetailsCheckViewMixin, EdcBaseViewMixin,
                         AdministrationViewMixin, TemplateView):
    pass
