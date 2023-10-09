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


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # not include in the Post or update

    class Meta:
        model = Cart
        fields = ["id"]  # select what you need in the get pyload


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cart = serializers.UUIDField(read_only=True)

    # product = serializers.IntegerField(read_only = True)
    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "quantity"]
