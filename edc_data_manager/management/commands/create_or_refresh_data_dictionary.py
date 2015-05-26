from optparse import make_option

from django.contrib import admin
from django.core.management.base import BaseCommand, CommandError

from ...classes import DataDictionary

from ...models import DataDictionaryModel


class Command(BaseCommand):

    args = '<app_label>, <app_label>, ...'
    help = 'Create data dictionaries for the given app_labels and save to data_dictionary.DataDictionaryModel.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        admin.autodiscover()
        for arg in args:
            dct = DataDictionary(arg)
            dct.save()
            self.stdout.write('Successfully create data dictionary for \'{0}\'. See data_dictionary.DataDictionaryModel.'.format(arg))
