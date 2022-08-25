from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class DataIssueListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    gabs = ListboardFilter(
        label='Gaborone',
        position=6,
        lookup={'site__id': 40})

    maun = ListboardFilter(
        label='Maun',
        position=6,
        lookup={'site__id': 41})

    serowe = ListboardFilter(
        label='Serowe',
        position=6,
        lookup={'site__id': 42})

    ghetto = ListboardFilter(
        label='Francistown',
        position=6,
        lookup={'site__id': 43})

    phikwe = ListboardFilter(
        label='Phikwe',
        position=6,
        lookup={'site__id': 44})
