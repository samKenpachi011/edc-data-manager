from django.db import models


from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_constants.constants import CLOSED, OPEN
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin


class DataActionItem(NonUniqueSubjectIdentifierFieldMixin, BaseUuidModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""

    action_date = models.DateField(
        verbose_name='Action date')

    comment = EncryptedTextField(max_length=500)

    display_on_dashboard = models.BooleanField(default=True)

    rt = models.IntegerField(default=0, verbose_name='RT Reference.')

    action_priority = models.CharField(
        max_length=35,
        choices=(('normal', 'Normal'), ('Medium', 'Medium'), ('high', 'High')),
        default='Normal')

    status = models.CharField(
        verbose_name="Status",
        max_length=35,
        choices=((OPEN, 'Open'), ('stalled', 'Stalled'), ('resolved', 'Resolved'), (CLOSED, 'Closed')),
        default=OPEN,
        help_text='Only data managers or study physicians can \'close\' an action item')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super(DataActionItem, self).save(*args, **kwargs)


    class Meta:
        app_label = "edc_data_manager"
