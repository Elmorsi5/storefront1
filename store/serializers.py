from decimal import Decimal
from rest_framework import serializers
from store.models import Cart, CartItem, Customer, Product, Collection, Order, Review


class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)

    # counts = serializers.SerializerMethodField(method_name="products_count")
    # def products_count(self,collection:Collection):
    #     return collection.products.count() # type: ignore


class ProductSerializers(
    serializers.ModelSerializer
):  # What field of product object to serialize = what field to include in the produced python dictionary?
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "inventory",
            "description",
            "unit_price",
            "price_with_tax",
            "collection",
            "collection_title",
        ]

    # Here you can override fields and add new one:-
    collection_title = serializers.SerializerMethodField(
        method_name="get_collection_name"
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = CollectionSerializers()  #applay this in each object and return the json as a refernce value
    # collection = serializers.StringRelatedField() #use select related in the query in your view
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

    def get_collection_name(self, product: Product):
        return product.collection.title


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["placed_at", "payment_status", "customer"]


class CustomerSrializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "membership",
            "orders_count",
        ]

    orders_count = serializers.IntegerField()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price",read_only = True)
    
    def get_total_price(self,cartitem:CartItem):
        return cartitem.quantity * cartitem.product.unit_price
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True, read_only = True)
    total_salary = serializers.SerializerMethodField()

    def get_total_salary(self,cart:Cart):
       return  sum([item.quantity * item.product.unit_price for item in cart.items.all()]) # type: ignore


    id = serializers.UUIDField(read_only=True)  # not include in the Post or update
    class Meta:
        model = Cart
        fields = ["id",'items','total_salary']  # select what you need in the get pyload


