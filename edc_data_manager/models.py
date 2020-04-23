from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.constants import CLOSED, OPEN
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base


class SearchSlugModelMixin(Base):

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('subject_identifier')
        return fields

    class Meta:
        abstract = True


class DataActionItemManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class ModelDiffMixin:
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                             self._meta.fields])

        

class DataActionItem(
        NonUniqueSubjectIdentifierFieldMixin, ModelDiffMixin, SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""

    subject = models.CharField(
        verbose_name="Issue Subject",
        max_length=100,)

    action_date = models.DateField(
        verbose_name='Action date',
        default=timezone.now
        )

    comment = EncryptedTextField(max_length=500)

    display_on_dashboard = models.BooleanField(default=True)

    issue_number = models.IntegerField(
        default=0,
        help_text="System auto field. Issue ref number.",)

    action_priority = models.CharField(
        max_length=35,
        choices=(('normal', 'Normal'), ('Medium', 'Medium'), ('high', 'High')),
        default='Normal')

    assigned = models.CharField(
        verbose_name="Assign to",
        max_length=50,)

    status = models.CharField(
        verbose_name="Status",
        max_length=35,
        choices=((OPEN, 'Open'), ('stalled', 'Stalled'), ('resolved', 'Resolved'), (CLOSED, 'Closed')),
        default=OPEN,
        help_text='Only data managers or study physicians can \'close\' an action item')

    objects = models.Manager()

    @property
    def snippet(self):
        return f'# {str(self.issue_number)}:  {self.subject}'

    def __str__(self):
        return f'#{self.issue_number}, {self.subject_identifier}'

    def save(self, *args, **kwargs):
        if not self.id:
            item = self.__class__.objects.all().order_by('issue_number').last()
            if item:
                last_item_number = item.issue_number
                self.issue_number = last_item_number + 1
            else:
                self.issue_number = 1
        super(DataActionItem, self).save(*args, **kwargs)
    
    @property
    def assign_users(self):
        """Reurn a list of users that can be assigned an issue.
        """
        assignable_users_choices = ()
        user = django_apps.get_model('auth.user')
        assignable_users = user.objects.filter(groups__name='assignable users')
        for assignable_user in assignable_users:
            username = assignable_user.username
            if not assignable_user.first_name:
                raise ValidationError(f"The user {username} needs to set their first name.")
            if not assignable_user.last_name:
                raise ValidationError(f"The user {username} needs to set their last name.")
            full_name = f'{assignable_user.first_name} {assignable_user.last_name}'
            assignable_users_choices += ((username, full_name),)
        return assignable_users_choices

    def email_users(self, instance=None, subject=None, message=None):
        """Send an email to users who are related to the issue created.
        """
        user = django_apps.get_model('auth.user')
        try:
            assugned_user = user.objects.get(username=instance.assigned)
        except user.DoesNotExist:
            raise ValidationError(
                f"The user {instance.assigned} that you have assigned the data issue {instance.issue_number}"
                " does not exist.")
        else:
            assigned_email = assugned_user.email
        try:
            created_user = user.objects.get(username=instance.user_created)
        except user.DoesNotExist:
            raise ValidationError(
                f"The user {instance.user_created} that created the data issue {instance.issue_number}"
                " does not exist.")
        else:
            created_email = created_user.email
        if created_email and assigned_email:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # FROM
                [assigned_email, created_email],  # TO
                fail_silently=False)


    class Meta:
        app_label = "edc_data_manager"
