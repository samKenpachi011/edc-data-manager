from ..models import TimePointStatus


class TimePointMixin(object):

    def save(self, *args, **kwargs):
        """Raises a ValidationError if timepoint is closed."""
        using = kwargs.get('using')
        try:
            TimePointStatus.check_time_point_status(self.visit.appointment, using=using)
        except AttributeError:
            TimePointStatus.check_time_point_status(self.appointment, using=using)
        super(TimePointMixin, self).save(*args, **kwargs)
