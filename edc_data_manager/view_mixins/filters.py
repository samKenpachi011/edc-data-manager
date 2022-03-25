from datetime import timedelta
import datetime

from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters

from ..models import DataActionItem, QueryName


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    gaborone = ListboardFilter(
        label='Gabs',
        position=10,
        lookup={'site__id': 40})

    maun = ListboardFilter(
        label='Maun',
        position=10,
        lookup={'site__id': 41})

    serowe = ListboardFilter(
        label='Serowe',
        position=10,
        lookup={'site__id': 42})

    francistown = ListboardFilter(
        label='F/Town',
        position=10,
        lookup={'site__id': 43})

    sphikwe = ListboardFilter(
        label='S/Phikwe',
        position=10,
        lookup={'site__id': 44})
        