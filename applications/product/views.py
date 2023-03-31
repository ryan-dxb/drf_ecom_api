from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
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

    @action(detail=False, methods=['get'], url_path=r'category/(?P<category>\w+)/all', url_name='all')
    def list_product_by_category(self, request, category=None):
        """
        A simple ViewSet for listing or retrieving categories by category.
        """

        filtered_queryset = self.queryset.filter(category__name=category)
        serializer = ProductSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
