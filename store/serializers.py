from decimal import Decimal
from rest_framework import serializers
from store.models import Product

class ProductSerializers(serializers.Serializer): #What field of product object to serialize = what field to include in the produced python dictionary?
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=6,decimal_places=2,source = 'unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)


