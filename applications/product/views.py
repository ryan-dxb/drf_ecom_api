from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# from django.db import connection
# from pygments import highlight
# from pygments.formatters import TerminalFormatter
# from pygments.lexers.sql import SqlLexer
# from sqlparse import format


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
    lookup_field = "slug"

    @extend_schema(responses=ProductSerializer(many=True))
    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class.data)

    # def retrieve(self, request, pk=None):
    #     """
    #     A simple ViewSet for listing or retrieving categories by pk.
    #     """

    #     filtered_queryset = self.queryset.filter(pk=pk)
    #     serializer = ProductSerializer(filtered_queryset, many=True)
    #     return Response(serializer.data)

    # Product by slug
    def retrieve(self, request, slug=None):
        """
        A simple ViewSet for listing or retrieving categories by slug.
        """

        filtered_queryset = (
            self.queryset.filter(slug=slug)
            .select_related("category", "brand")
            .prefetch_related("product_line")
        )
        serializer = ProductSerializer(filtered_queryset, many=True)

        resData = Response(serializer.data)

        # queries = list(connection.queries)

        # print("Total queries: ", len(queries))

        # for query in queries:
        #     sqlformatted = format(str(query["sql"]), reindent=True)

        #     # Show the SQL query
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return resData

    @action(
        detail=False,
        methods=["get"],
        url_path=r"category/(?P<category>\w+)/all",
        url_name="all",
    )
    def list_product_by_category(self, request, category=None):
        """
        A simple ViewSet for listing or retrieving categories by category.
        """

        filtered_queryset = self.queryset.filter(category__name=category)
        serializer = ProductSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
