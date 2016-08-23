from django.contrib import admin
from django.contrib.auth.models import Group

from edc_constants.constants import CLOSED, OPEN
from edc_registration.models import RegisteredSubject

from .forms import ActionItemForm
from .models import ActionItem, Comment

from .data_manager import data_manager


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        pass


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):

    form = ActionItemForm

    fields = [
        'registered_subject', 'subject', 'action_date', 'expiration_date', 'action_priority',
        'status', 'comment', 'action_group', 'rt']

    list_display = ['created', 'subject', 'dashboard', 'rt', 'status', 'user_created', 'user_modified', 'modified']

    list_filter = ['status', 'action_group', 'created', 'user_created', 'modified', 'user_modified']

    search_fields = ('registered_subject__pk', 'registered_subject__subject_identifier')

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
