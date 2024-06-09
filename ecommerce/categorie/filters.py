import django_filters
from .models import Categories

class CategoriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Categories
        fields = ['name']
