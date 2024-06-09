from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import SuperMarket
from .serializers import SuperMarketSerializer
from .filters import SuperMarketFilter

class SuperMarketViewSet(viewsets.ModelViewSet):
    queryset = SuperMarket.objects.all()
    serializer_class = SuperMarketSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SuperMarketFilter


