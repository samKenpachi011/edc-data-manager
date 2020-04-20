from django.contrib import admin

from edc_base.sites.admin import ModelAdminSiteMixin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_subject_dashboard import ModelAdminSubjectDashboardMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSubjectDashboardMixin, ModelAdminSiteMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

from .forms import DataActionItemForm
from .models import DataActionItem
from .admin_site import edc_data_manager_admin


@admin.register(DataActionItem, site=edc_data_manager_admin)
class DataActionItemAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = DataActionItemForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'action_date',
                'action_priority',
                'status',
                'comment',
                'rt')}),
        audit_fieldset_tuple
    )

    list_display = ['created', 'subject_identifier', 'rt', 'status', 'user_created', 'user_modified', 'modified']

    list_filter = ['status', 'created', 'user_created', 'modified', 'user_modified']

    search_fields = ('subject_identifier',)
