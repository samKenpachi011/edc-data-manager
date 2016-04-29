from django.contrib.auth.models import Group
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError
from django.db.utils import OperationalError, ProgrammingError


class DataManager(object):
    def prepare(self):
        """Adds 'data_manager' and 'action_manager' groups if missing.

        These groups are referred to in ActionItemAdmin.save_model().

        Add this to project urls.py before admin.autodiscover()::

            from edc_data_manager.data_manager import data_manager
            data_manager.prepare()
        """

        try:
            Group.objects.create(name='data_manager')
        except IntegrityError:
            pass
        except OperationalError:
            pass
        except ProgrammingError:
            pass
        try:
            Group.objects.create(name='action_manager')
        except IntegrityError:
            pass
        except OperationalError:
            pass
        except ProgrammingError:
            pass

    def check_groups(self):
        """Raises error if 'data_manager' and 'action_manager' groups are missing."""

        if not Group.objects.filter(name='data_manager').exists():
            raise ImproperlyConfigured(
                'Group \'data_manager\' does not exist. Add data_manager.prepare() '
                'to your urls.py before admin.autodiscover(). See data_manager.')
        if not Group.objects.filter(name='action_manager').exists():
            raise ImproperlyConfigured(
                'Group \'action_manager\' does not exist. Add data_manager.prepare() '
                'to your urls.py before admin.autodiscover(). See data_manager.')
        return True

data_manager = DataManager()
