from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuperMarketViewSet

router = DefaultRouter()
router.register(r'supermarkets', SuperMarketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
