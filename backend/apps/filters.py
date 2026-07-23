from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    brand = filters.CharFilter(lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    # bo'lim bo'yicha: ?department=<bo'lim id>
    department = filters.NumberFilter(field_name='category__parent')

    class Meta:
        model = Product
        fields = ['category', 'department', 'brand', 'unit', 'is_active']
