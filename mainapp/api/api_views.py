from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import CategorySerializers, ResistorSerializer, CustomerSerializer
from ..models import Category, Resistor, Customer


# Знакомство с пагинацией
class CategoryPagination(PageNumberPagination):
    page_size = 2
    page_size_query_description = 'page_size'
    max_page_size = 10


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializers
    pagination_class = CategoryPagination
    queryset = Category.objects.all()


class ResistorAPIView(ListAPIView):
    serializer_class = ResistorSerializer
    queryset = Resistor.objects.all()
    filter_backends = [SearchFilter]
    search_fields = [
        'price', 'title'
    ]
    """
    одна из возможных реализаций поиска
        def get_queryset(self):
        qs = super(ResistorAPIView, self).get_queryset()
        price = self.request.query_params.get('price')
        return qs.filter(price__iexact=price)
    """


class ResistorDetailAPIView(RetrieveAPIView):
    serializer_class = ResistorSerializer
    queryset = Resistor.objects.all()
    lookup_field = 'id'


class CustomerListAPIView(ListAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()