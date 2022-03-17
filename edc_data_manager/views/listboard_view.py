import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from django_pandas.io import read_frame

from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import CLOSED, OPEN
from edc_navbar import NavbarViewMixin

from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView

from ..model_wrappers import DataActionItemModelWrapper
from ..models import DataActionItem
from ..view_mixins import UserDetailsCheckViewMixin


class ListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, UserDetailsCheckViewMixin,
                    SearchFormViewMixin, ListboardView):

    listboard_template = 'data_manager_listboard_template'
    listboard_url = 'data_manager_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'edc_data_manager.dataactionitem'
    model_wrapper_cls = DataActionItemModelWrapper
    navbar_name = 'edc_data_manager'
    navbar_selected_item = 'data_manager'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'data_manager_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @property
    def query_summary(self):
        """Return a summary of quesries
        """
        data = []
        qs_categories = DataActionItem.objects.all().values_list('query_name', flat=True)
        qs_categories = list(set(qs_categories))
        for query_name in qs_categories:
            qs_gabs = DataActionItem.objects.filter(site__id=40, query_name=query_name)
            qs_maun = DataActionItem.objects.filter(site__id=41, query_name=query_name)
            qs_serowe = DataActionItem.objects.filter(site__id=42, query_name=query_name)
            qs_gheto = DataActionItem.objects.filter(site__id=43, query_name=query_name)
            qs_sphikwe = DataActionItem.objects.filter(site__id=44, query_name=query_name)
            qs = DataActionItem.objects.filter(query_name=query_name)
            data.append([
                query_name, qs_gabs.count(), qs_maun.count(),
                qs_serowe.count(), qs_gheto.count(), qs_sphikwe.count(),
                qs.count()])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_action_items = DataActionItem.objects.filter(status=OPEN)
        stalled_action_items = DataActionItem.objects.filter(status='stalled')
        resolved_action_items = DataActionItem.objects.filter(status='resolved')
        closed_action_items = DataActionItem.objects.filter(status=CLOSED)
        context.update(
            query_summary=self.query_summary,
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

    def get_wrapped_queryset(self, queryset):
        """Returns a list of wrapped model instances.
        """
        object_list = []

        for obj in queryset:
            if obj.subject_type == 'infant':
                next_url_name = settings.DASHBOARD_URL_NAMES.get(
                    'infant_subject_dashboard_url')
            else:
                next_url_name = settings.DASHBOARD_URL_NAMES.get(
                    'subject_dashboard_url')
            object_list.append(self.model_wrapper_cls(obj,
                                                      next_url_name=next_url_name))
        return object_list
