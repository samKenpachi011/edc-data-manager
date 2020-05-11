from django.apps import apps as django_apps
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.base import ContextMixin


class UserDetailsCheckViewMixin(ContextMixin):

    @property
    def assignable_users(self):
        """Reurn users that belong to the action item assignable group.
        """
        app_config = django_apps.get_app_config('edc_data_manager')
        assignable_users_group = app_config.assignable_users_group
        return User.objects.filter(
            groups__name=assignable_users_group)

    @property
    def fix_email_msg(self):
        """Return a list of users that need their emails updated.
        """
        fix_email_msg = 'Set or update emails of the following users: '
        usernames = ''
        for user in self.assignable_users:
            if not user.email:
                usernames += user.username + ','
        if usernames:
            fix_email_msg += usernames
        else:
            fix_email_msg = None
        return fix_email_msg

    @property
    def fix_usernames_msg(self):
        """Return all users who need to update their first name of last name.
        """
        fix_usernames_msg = (
            'Set or update first name/last names of the following users: ')
        usernames = ''
        for user in self.assignable_users:
            if not user.first_name and not user.last_name:
                usernames += user.username + ','
        if usernames:
            fix_usernames_msg += usernames
        else:
            fix_usernames_msg = None
        return fix_usernames_msg

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.fix_email_msg:
            messages.add_message(
                self.request, messages.ERROR, self.fix_email_msg)
        if self.fix_usernames_msg:
            messages.add_message(
                self.request, messages.ERROR, self.fix_usernames_msg)
        if not self.assignable_users:
            app_config = django_apps.get_app_config('edc_data_manager')
            assignable_users_group = app_config.assignable_users_group
            msg = (
                'To assign users data action items add the to a group: '
                f'{assignable_users_group}')
            messages.add_message(
                self.request, messages.ERROR, msg)
        return context
