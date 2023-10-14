from django_filters.rest_framework import FilterSet
from .models import Customer, Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id':['exact'],
            'unit_price':['gt','lt']
        }

class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = {
            'user__email':['exact'],
            'phone':['exact']
        }