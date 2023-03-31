from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Brand, Product
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer(queryset, many=True)

    @extend_schema(responses=CategorySerializer(many=True))
    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer(queryset, many=True)

    @extend_schema(responses=BrandSerializer(many=True))
    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class.data)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer(queryset, many=True)

    @extend_schema(responses=ProductSerializer(many=True))
    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class.data)
