from decimal import Decimal
from rest_framework import serializers
from store.models import Customer, Product,Collection, Order


class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']
    
    products_count = serializers.IntegerField()

    # counts = serializers.SerializerMethodField(method_name="products_count")
    # def products_count(self,collection:Collection):
    #     return collection.products.count() # type: ignore


class ProductSerializers(serializers.ModelSerializer): #What field of product object to serialize = what field to include in the produced python dictionary?
    class Meta:
        model = Product
        fields = ['id','title','slug','inventory','description','unit_price','price_with_tax','collection','collection_title']

    #Here you can override fields and add new one:-
    collection_title = serializers.SerializerMethodField(method_name="get_collection_name")
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = CollectionSerializers()  #applay this in each object and return the json as a refernce value
    # collection = serializers.StringRelatedField() #use select related in the query in your view
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    def calculate_tax(self,product:Product):
        return product.unit_price * Decimal(1.1)
    
    def get_collection_name(self,product:Product):
        return product.collection.title


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['placed_at','payment_status','customer']


class CustomerSrializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name','last_name','email','phone','birth_date','membership','orders_count']
    orders_count = serializers.IntegerField()
    
