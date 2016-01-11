from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.db import models

from edc_base.encrypted_fields import EncryptedTextField
from edc_base.model.models import BaseModel
from edc_constants.constants import CLOSED, OPEN
from edc_registration.models import RegisteredSubject


class Comment(BaseModel):

    subject = models.CharField(max_length=50)
    comment_date = models.DateField(default=date.today())
    comment = EncryptedTextField(max_length=500)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    status = models.CharField(
        max_length=35,
        choices=(('Open', 'Open'), ('Stalled', 'Stalled'), ('Resolved', 'Resolved')),
        default='Open')
    objects = models.Manager()

    class Meta:
        app_label = "data_manager"


class ActionItem(BaseModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""
    registered_subject = models.ForeignKey(RegisteredSubject)
    subject = models.CharField(verbose_name='Subject line', max_length=50, unique=True)
    action_date = models.DateField(verbose_name='action_date', default=date.today())
    expiration_date = models.DateField(default=date.today() + timedelta(days=90), help_text='Data note will automatically be set to \'Resolved\' in 90 days unless otherwise specified.')
    comment = EncryptedTextField(max_length=500)
    display_on_dashboard = models.BooleanField(default=True)
    rt = models.IntegerField(default=0, verbose_name='RT Ref.')
    action_priority = models.CharField(
        max_length=35,
        choices=(('normal', 'Normal'), ('Medium', 'Medium'), ('high', 'High')),
        default='Normal')
    action_group = models.CharField(
        max_length=35,
        # choices=[(item.get('name'), ' '.join(item.get('name').split('_'))) for item in Group.objects.values('name').all()] + [('no group', '<no group>')],
        default='no group',
        help_text='You can only select a group to which you belong. Choices are based on Groups defined in Auth.')
    status = models.CharField(
        max_length=35,
        choices=((OPEN, 'Open'), ('stalled', 'Stalled'), ('resolved', 'Resolved'), (CLOSED, 'Closed')),
        default=OPEN,
        help_text='Only data managers or study physicians can \'close\' an action item')
    objects = models.Manager()

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('subject_dashboard_url',
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                      'dashboard_model': 'registered_subject',
                                      'dashboard_id': self.registered_subject.pk,
                                      'show': 'appointments'})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = "data_manager"
