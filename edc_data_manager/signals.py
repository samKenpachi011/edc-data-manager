from django.apps import apps as django_apps
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from edc_base import get_utcnow

from .models import DataActionItem


@receiver(post_save, weak=False, sender=DataActionItem,
          dispatch_uid='data_action_item_on_post_save')
def data_action_item_on_post_save(sender, instance, raw, created, **kwargs):
    app_config = django_apps.get_app_config('edc_data_manager')
    email_issue_notification = app_config.email_issue_notification
    if not raw and app_config.assianable_users_note:
        emails = []
        extra_assignee_choices = django_apps.get_app_config(
            'edc_data_manager').extra_assignee_choices
        if extra_assignee_choices:
            for key, value in extra_assignee_choices.items():
                if instance.assigned == key:
                    emails += value[1]
        if created:
            if emails:
                subject = (
                    f"Issue number: {instance.issue_number}. {instance.subject}"
                    f" has been assigned to {instance.assigned} by "
                    f"{instance.user_created}")
                message = f"{instance.comment}"
                instance.email_users(
                    instance=instance, subject=subject,
                    message=message, emails=emails)
            else:
                subject = (f"Issue number: {instance.issue_number}. "
                           f"{instance.subject} has been assigned to "
                           f"{instance.assigned} by {instance.user_created}")
                message = f"{instance.comment}"
                instance.email_users(
                    instance=instance, subject=subject, message=message)
        else:
            change_message = ""
            subject = (
                f"Issue number: {instance.issue_number}. {instance.subject}"
                f" has been assigned to you by {instance.user_created}")
            if instance.has_changed:
                changed_fields = instance.changed_fields
                count = 1
                for changed_field in changed_fields:
                    old_value = instance.get_field_diff(changed_field)[0]
                    change = instance.get_field_diff(changed_field)[1]
                    msg = (f"{count}. value for {changed_field} has been "
                           f"updated from {old_value} to {change}. \r\n")
                    count += 1
                    change_message += msg
                message = f"{change_message} \r\n \r\n \r\n {instance.comment}"
                if emails and email_issue_notification:
                    instance.email_users(
                        instance=instance, subject=subject,
                        message=message, emails=emails)
                else:
                    instance.email_users(
                        instance=instance, subject=subject, message=message)


@receiver(pre_save, weak=False, sender=DataActionItem,
          dispatch_uid='data_action_item_on_pre_save')
def data_action_item_on_pre_save(sender, instance, raw, using, **kwargs):
    if not raw:
        if instance.status == 'resolved':
            if instance.date_resolved is None:
                instance.date_resolved = get_utcnow().date()
            elif (instance.date_resolved and
                  instance.history.latest('history_date').date_resolved):
                instance.date_resolved = get_utcnow().date()
        if instance.status == 'closed':
            if instance.date_closed is None:
                instance.date_closed = get_utcnow().date()
            elif (instance.date_closed and
                  instance.history.latest('history_date').date_closed):
                instance.date_closed = get_utcnow().date()
