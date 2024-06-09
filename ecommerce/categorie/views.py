from rest_framework import viewsets
from .models import Categories
from .serializers import CategoriesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoriesFilter

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoriesFilter
