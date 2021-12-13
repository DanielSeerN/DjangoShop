from collections import OrderedDict

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer
from ..models import Category, Product, Customer


class CategoryPaginaiton(PageNumberPagination):
    """
    Пагинация для API категории
    """
    page_size = 1
    page_query_param = 'page_size'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('quantity', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class CategoryAPIView(ListCreateAPIView):
    """
    API-представление для категории продукта
    """
    queryset = Category.objects.all()
    pagination_class = CategoryPaginaiton
    serializer_class = CategorySerializer


class ProductAPIView(ListAPIView):
    """
    API-представление для продукта
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class CustomerAPIView(ListAPIView):
    """
    API-представление для покупателя
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
