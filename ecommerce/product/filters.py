import django_filters
from .models import Products

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='categories__name', lookup_expr='icontains')
    prix_min = django_filters.NumberFilter(field_name='prix', lookup_expr='gte')
    prix_max = django_filters.NumberFilter(field_name='prix', lookup_expr='lte')

    class Meta:
        model = Products
        fields = ['name', 'category', 'prix_min', 'prix_max']
