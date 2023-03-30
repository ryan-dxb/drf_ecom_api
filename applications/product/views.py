from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving categories.
    """
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer(many=True))
    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        return Response(self.serializer_class(queryset, many=True).data)
