from django.db import models
from django.utils import timezone


from django_crypto_fields.fields import EncryptedTextField
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.constants import CLOSED, OPEN
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager
from edc_search.model_mixins import SearchSlugModelMixin as Base
from django.db.models.aggregates import Max


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


class DataActionItem(
        NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin, SearchSlugModelMixin, BaseUuidModel):
    """ Tracks notes on missing or required data.

    Note can be displayed on the dashboard"""

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

    status = models.CharField(
        verbose_name="Status",
        max_length=35,
        choices=((OPEN, 'Open'), ('stalled', 'Stalled'), ('resolved', 'Resolved'), (CLOSED, 'Closed')),
        default=OPEN,
        help_text='Only data managers or study physicians can \'close\' an action item')

    objects = models.Manager()

    @property
    def snippet(self):
        return '#' + str(self.issue_number) + ': ' + self.description[:12] + " ..."

    def save(self, *args, **kwargs):
        if not self.id:
            item = self.objects.all().order_by('number').last()
            if item:
                last_item_number = item.issue_number
                self.issue_number = last_item_number + 1
            else:
                self.issue_number = 1
        super(DataActionItem, self).save(*args, **kwargs)


    class Meta:
        app_label = "edc_data_manager"
