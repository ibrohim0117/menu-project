from django_filters import rest_framework as filters
from .models import MenuItem

class MenuItemFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='ltg')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')