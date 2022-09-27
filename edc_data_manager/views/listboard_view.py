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
from edc_dashboard.listboard_filter import ListboardFilter
from requests import delete

from .reports_mixins.resolved_daily_mixin import ResolvedDailyMixin
from ..model_wrappers import DataActionItemModelWrapper
from ..models import DataActionItem, QueryName
from ..view_mixins import ListboardViewFilters, UserDetailsCheckViewMixin


class ListBoardView(NavbarViewMixin, ResolvedDailyMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, UserDetailsCheckViewMixin,
                    SearchFormViewMixin, ListboardView):
    listboard_template = 'data_manager_listboard_template'
    listboard_url = 'data_manager_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    listboard_view_filters = ListboardViewFilters()
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
        qs_categories = DataActionItem.objects.values_list('query_name', flat=True)
        qs_categories = list(set(qs_categories))
        active_queries = DataActionItem.objects.filter(status__in=['resolved', 'stalled', OPEN])
        for query_name in qs_categories:
            qs_gabs = active_queries.filter(site__id=40, query_name=query_name)
            qs_maun = active_queries.filter(site__id=41, query_name=query_name)
            qs_serowe = active_queries.filter(site__id=42, query_name=query_name)
            qs_gheto = active_queries.filter(site__id=43, query_name=query_name)
            qs_sphikwe = active_queries.filter(site__id=44, query_name=query_name)
            qs = active_queries.filter(query_name=query_name)
            data.append([
                query_name, qs_gabs.count(), qs_maun.count(),
                qs_serowe.count(), qs_gheto.count(), qs_sphikwe.count(),
                qs.count()])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_action_items = DataActionItem.objects.filter(
            status=OPEN, site_id=self.site_id)
        stalled_action_items = DataActionItem.objects.filter(
            status='stalled', site_id=self.site_id)
        resolved_action_items = DataActionItem.objects.filter(
            status='resolved', site_id=self.site_id)
        closed_action_items = DataActionItem.objects.filter(
            status=CLOSED, site_id=self.site_id)
        context.update(
            resolved_last_week=self.resolved_last_week,
            closed_last_week=self.closed_last_week,
            query_summary=self.query_summary,
            export_add_url=self.model_cls().get_absolute_url(),
            open_action_items=open_action_items.count(),
            stalled_action_items=stalled_action_items.count(),
            resolved_action_items=resolved_action_items.count(),
            closed_action_items=closed_action_items.count(),
            query_names=self.get_query_names)
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)

        del options['site']

        if kwargs.get('subject_identifier', None):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})

        status = request.GET.get('status', None)

        query_name = request.GET.get('query_name', None)

        if status:
            options.update(
                {'status': status})

        if query_name:
            options.update(
                {'query_name': query_name})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    @property
    def get_query_names(self):
        query_names = DataActionItem.objects.values_list('query_name', flat=True).distinct()
        return query_names

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

    @property
    def site_id(self):
        return settings.SITE_ID
