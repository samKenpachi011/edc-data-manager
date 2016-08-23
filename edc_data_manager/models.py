from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError

from django_crypto_fields.fields import EncryptedTextField
from edc_base.model.models import BaseModel
from edc_constants.constants import CLOSED, OPEN
from edc_registration.mixins import RegisteredSubjectMixin
from edc_base.model.models.base_uuid_model import BaseUuidModel


class Comment(BaseModel):

    subject = models.CharField(max_length=50)

    comment_date = models.DateField(default=date.today)

    comment = EncryptedTextField(max_length=500)

    rt = models.IntegerField(default=0, verbose_name='RT Ref.')

    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    class Meta:
        app_label = "edc_data_manager"


class ActionItem(RegisteredSubjectMixin, BaseUuidModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""

    subject = models.CharField(verbose_name='Subject line', max_length=50, unique=True)

    action_date = models.DateField(verbose_name='action_date', default=date.today)

    expiration_date = models.DateField(
        null=True,
        help_text=(
            'Data note will automatically be set to '
            'expire in 30 days from the action date unless otherwise specified.'))

    comment = EncryptedTextField(max_length=500)

    display_on_dashboard = models.BooleanField(default=True)

    rt = models.IntegerField(default=0, verbose_name='RT Ref.')

    action_priority = models.CharField(
        max_length=35,
        choices=(('normal', 'Normal'), ('Medium', 'Medium'), ('high', 'High')),
        default='Normal')

    action_group = models.CharField(
        max_length=35,
        default='no group',
        help_text=(
            'You can only select a group to which you belong. '
            'Choices are based on Groups defined in Auth.'))

    status = models.CharField(
        max_length=35,
        choices=((OPEN, 'Open'), ('stalled', 'Stalled'), ('resolved', 'Resolved'), (CLOSED, 'Closed')),
        default=OPEN,
        help_text='Only data managers or study physicians can \'close\' an action item')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = self.action_date + timedelta(days=30)
        else:
            if self.expiration_date < self.action_date:
                raise ValidationError('Expiration date cannot precede action date. Perhaps catch this in the forms.py')
        super(ActionItem, self).save(*args, **kwargs)

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.subject_type.lower(),
                              'dashboard_model': 'registered_subject',
                              # 'dashboard_id': self.registered_subject.pk,
                              'show': 'appointments'})
        ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = "edc_data_manager"
