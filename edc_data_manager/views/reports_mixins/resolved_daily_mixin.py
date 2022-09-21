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
        items = DataActionItem.objects.filter(status='resolved', site_id=settings.SITE_ID)
        resolved = []
        for item in items:
            init = [resolved.history_date for resolved in
                    item.history.filter(status='resolved',
                                        history_date__lte=datetime.datetime.today(),
                                        history_date__gt=datetime.datetime.today() - datetime.timedelta(
                                            days=7)) if
                    getattr(resolved.prev_record, 'status') != 'resolved']
            resolved.append(max(init).date())
        rc = Counter()
        rc.update(resolved)
        return rc

    @property
    def closed_last_week(self):
        cl_items = DataActionItem.objects.filter(status='closed')
        closed = []
        for item in cl_items:
            init = [closed.history_date for closed in item.history.filter(
                status='closed', history_date__lte=datetime.datetime.today(),
                history_date__gt=datetime.datetime.today() - datetime.timedelta(
                    days=7))
                    if getattr(closed.prev_record, 'status') != 'closed']
            closed.append(max(init).date())
        cc = Counter()
        cc.update(closed)
        return cc
