import datetime
from collections import Counter

from django.db.models import Count
from django.db.models.functions import TruncDate
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import CLOSED
from django.conf import settings
from edc_data_manager.models import DataActionItem


class ResolvedDailyMixin:

    @property
    def resolved_last_week(self):
        return DataActionItem.objects.filter(
            site_id=settings.SITE_ID, status='resolved', date_resolved__lte=datetime.datetime.today().date(),
            date_resolved__gt=datetime.datetime.today().date() - datetime.timedelta(
                days=7)).annotate(day=TruncDate('date_resolved'), ).values('day').annotate(
            n=Count('id')).order_by('day')

    @property
    def closed_last_week(self):
        return DataActionItem.history.filter(
            site_id=settings.SITE_ID, status=CLOSED, date_closed__lte=datetime.datetime.today().date(),
            date_closed__gt=datetime.datetime.today().date() - datetime.timedelta(
                days=7)).annotate(day=TruncDate('date_closed'), ).values('day').annotate(
            n=Count('id')).order_by('day')
