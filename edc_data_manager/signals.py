from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import DataActionItem


@receiver(post_save, weak=False, sender=DataActionItem,
          dispatch_uid='data_action_item_on_post_save')
def data_action_item_on_post_save(sender, instance, raw, created, **kwargs):
    """Creates a protocol response.
    """
    if not raw:
        if created:
            subject = (
                f"Issue number: {instance.issue_number}. {instance.subject}"
                f" has been assigned to {instance.assigned} by {instance.user_created}")
            message = f"{instance.comment}"
            instance.email_users(instance=instance, subject=subject, message=message)
        else:
            change_message = ""
            subject = (
                f"Issue number: {instance.issue_number}. {instance.subject}"
                f" has been assigned to you by {instance.user_created}")
            if instance.has_changed:
                changed_fields = instance.changed_fields
                count = 1
                for changed_field in changed_fields:
                    change = instance.get_field_diff(changed_field)[1]
                    count += 1
                    msg = f"{count}. value for {changed_field} has been updated to {change}."
                    change_message += msg
                message = f"{change_message} \r\n {instance.comment}"
                instance.email_users(instance=instance, subject=subject, message=message)