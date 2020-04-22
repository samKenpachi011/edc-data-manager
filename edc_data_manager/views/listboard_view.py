import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import CLOSED, OPEN
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ..model_wrappers import DataActionItemModelWrapper
from ..models import DataActionItem


class ListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin, ListboardView):

    listboard_template = 'data_manager_listboard_template'
    listboard_url = 'data_manager_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'edc_data_manager.dataactionitem'
    model_wrapper_cls = DataActionItemModelWrapper
    navbar_name = 'data_manager'
    navbar_selected_item = 'data_management'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'data_manager_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_action_items = DataActionItem.objects.filter(status=OPEN)
        stalled_action_items = DataActionItem.objects.filter(status='stalled')
        resolved_action_items = DataActionItem.objects.filter(status='resolved')
        closed_action_items = DataActionItem.objects.filter(status=CLOSED)
        context.update(
            export_add_url=self.model_cls().get_absolute_url(),
            open_action_items=open_action_items.count(),
            stalled_action_items=stalled_action_items.count(),
            resolved_action_items=resolved_action_items.count(),
            closed_action_items=closed_action_items.count())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
