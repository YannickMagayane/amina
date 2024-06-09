# filters.py
import django_filters
from .models import SuperMarket

class SuperMarketFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    localisation = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = SuperMarket
        fields = ['name', 'localisation']
