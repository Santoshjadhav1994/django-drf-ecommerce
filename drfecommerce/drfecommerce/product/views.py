from rest_framework import viewsets
from .models import Brand, Category, Product
from drf_spectacular.utils import extend_schema
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer
from sqlparse import format

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    A simple Viewset for viewing all brand
    """

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    
    """
    A simple Viewset for viewing all products
    """

    queryset = Product.objects.all().isactive()
    
    lookup_field = "slug"

    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related("category", "brand"),
            many=True,
        )
        data = Response(serializer.data)

        q = list(connection.queries)
        print(len(q))
        # for qs in q:
        #     sqlformatted = format(str(qs["sql"]), reindent=True)
        #     print(highlight(sqlformatted, SqlLexer(), TerminalFormatter()))

        return data

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path=r"category/(?P<slug>[\w-]+)",
    )
    def list_product_by_category_slug(self, request, slug=None):
        """
        An endpoint to return product by category
        """
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug), many=True
        )
        return Response(serializer.data)