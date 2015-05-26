from optparse import make_option

from django.contrib import admin
from django.core.management.base import BaseCommand, CommandError

from ...classes import FormExporter


class Command(BaseCommand):

    help = 'Export forms in wiki text format given a visit code or app_label.model_name.'

    option_list = BaseCommand.option_list + (
        make_option('--visit',
            action='store',
            dest='by_visit',
            default='',
            help='Export form text by visit code'),
        make_option('--model',
            action='store',
            dest='by_model',
            default='',
            help='Export form text by app_label.model_name'),
        make_option('--app',
            action='store',
            dest='by_app',
            default='',
            help='Export form text by app_label'),
        )
#         make_option('--fields',
#             action='store',
#             dest='by_app',
#             default='',
#             help='specify name of modeladmin fields attribute of not "fields"'),

    def handle(self, *args, **options):
        admin.autodiscover()
        try:
            if options['by_visit']:
                try:
                    f = FormExporter()
                    for form in f.export_by_visit(options['by_visit']):
                        for line in form:
                            print line
                        print '\n'
                except IndexError:
                    raise CommandError('Expected visit code. Got None.')
            elif options['by_app']:
                try:
                    f = FormExporter()
                    for opt in options['by_app'].split(','):
                        for form in f.export_by_app(opt):
                            for line in form:
                                print line
                            print '\n'
                except IndexError:
                    raise CommandError('Expected visit code. Got None.')
            elif options['by_model']:
                try:
                    f = FormExporter()
                    for model in options['by_model'].split(','):
                        for form in f.export_by_model(*model.split('.')):
                            for line in form:
                                print line
                            print '\n'
                except IndexError:
                    raise CommandError('Expected visit code. Got None.')
            else:
                raise CommandError('At least one option is required.')
        except KeyError:
            raise CommandError('Unknown or missing option.')
