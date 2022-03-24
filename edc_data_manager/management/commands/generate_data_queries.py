from django.core.management.base import BaseCommand

from ...classes import  QueryGeneration


class Command(BaseCommand):

    help = 'Generate queries'

    def handle(self, *args, **kwargs):
        queries = QueryGeneration()
        print("Generating queries for missing visit forms")
        queries.missing_visit_forms
        print('Done')



