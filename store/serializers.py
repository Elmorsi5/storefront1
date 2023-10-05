from decimal import Decimal
from rest_framework import serializers
from store.models import Product,Collection


class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','featured_product']


class ProductSerializers(serializers.ModelSerializer): #What field of product object to serialize = what field to include in the produced python dictionary?
    class Meta:
        model = Product
        fields = ['id','title','slug','inventory','description','unit_price','price_with_tax','collection']

    #Here you can override fields and add new one:-

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializers()  #applay this in each object and return the json as a refernce value
    # collection = serializers.StringRelatedField() #use select related in the query in your view
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)


