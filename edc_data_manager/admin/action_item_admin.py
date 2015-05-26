from django.contrib import admin
from django.contrib.auth.models import Group

from edc_constants.constants import CLOSED, OPEN
from edc_registration.models import RegisteredSubject

from ..classes import data_manager
from ..forms import ActionItemForm
from ..models import ActionItem

from .base_admin import BaseAdmin


class ActionItemAdmin(BaseAdmin):

    form = ActionItemForm

    def __init__(self, *args, **kwargs):
        super(ActionItemAdmin, self).__init__(*args, **kwargs)
        self.search_fields.insert(0, 'registered_subject__pk')
        self.search_fields.insert(0, 'registered_subject__subject_identifier')
        self.list_display.insert(1, 'dashboard')
        self.list_filter.append('action_group')

    def save_model(self, request, obj, form, change):
        # check for data_manager user groups
        # group = data_manager.prepare()
        data_manager.check_groups()
        user = request.user
        if not user.is_superuser:
            # A user should be able to assign an action item to any other user group
            user_groups = [group.name for group in Group.objects.all()]
#             user_groups = [group.name for group in Group.objects.filter(user__username=request.user)]
            if not user_groups:
                obj.action_group = 'no group'
            elif obj.action_group not in user_groups:
                obj.action_group = user_groups[0]
            else:
                pass
            if obj.status == CLOSED and ('data_manager' not in user_groups and 'action_manager' not in user_groups):
                obj.status = OPEN
        super(ActionItemAdmin, self).save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "registered_subject":
            if request.GET.get('registered_subject'):
                kwargs["queryset"] = RegisteredSubject.objects.filter(pk=request.GET.get('registered_subject'))
        return super(ActionItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ActionItem, ActionItemAdmin)
