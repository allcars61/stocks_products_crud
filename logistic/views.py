from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product, Stock
from .serializers import ProductSerializer, StockSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["positions__product_id"]
    search_fields = ["positions__product__title"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related("positions")
