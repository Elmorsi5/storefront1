from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin,
)
from store.filters import CustomerFilter, ProductFilter
from store.pagination import CustomerPagination, ProductPagination
from .serializers import (
    CartItemSerializer,
    CartSerializer,
    OrderSerializer,
    ProductSerializers,
    CollectionSerializers,
    CustomerSrializer,
    ReviewSerializer,
)
from .models import Cart, CartItem, Product, Collection, Customer, Order, Review
from django.db.models import Count


# Create your views here:
# 1-Function Based
# 2-Class Based APIView
# 3-mixins - generic APIViews
# 4-Viewset


# 1- Using [Function Based View] [manually handle http methods and manually write the functionsto : [list- create - update - Delete] ]
@api_view(["GET", "POST"])
def customer_list(request):
    if request.method == "GET":
        queryset = Customer.objects.annotate(
            orders_count=Count("orders")).all()
        serializer = CustomerSrializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CustomerSrializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return (serializer.data, status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def customer_detail(request, id):
    queryset = Customer.objects.annotate(orders_count=Count("orders"))
    customer = get_object_or_404(queryset, pk=id)
    if request.method == "GET":
        serializer = CustomerSrializer(customer)
        return Response(serializer.data, status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = CustomerSrializer(customer, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
    elif request.method == "DELETE":
        if customer.orders.count() > 0:  # type: ignore
            return Response(
                {"error": "can't delete this user as it have order in progress"},
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        customer.delete()
        return Response(status.HTTP_204_NO_CONTENT)


# ----------------------------------------------------------------------------


# 2-Using [Class APIView] Class [no more of (if conditions) to handle http methods ]
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializers(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializers(product)
        return Response(serializer.data, status.HTTP_200_OK)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if self.product.orders.count() > 0:  # type: ignore
            return Response(
                {"error": "you can't delete it as you have purhsed it"},
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        else:
            product.delete()
            return Response(status.HTTP_204_NO_CONTENT)


class ReviewList(APIView):
    class ReviewSerializer(serializers.ModelSerializer):
        class Meta:
            model = Review
            fields = ["id", "date", "name", "description"]

    def get(self, requeset):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ----------------------------------------------------------------------------


# 3-[GenericAPIView] [built in function do work,only provide unique(queryset-serializer_class -lookup_field) and Customize built in function if need]
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count("products")).all()
    serializer_class = CollectionSerializers

    # We use it to provide the serializer with data that it need:
    def get_serializer_context(self):
        return {"request": self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count("products")).all()
    serializer_class = CollectionSerializers

    def delete(self, request, id):
        collection = get_object_or_404(self.queryset, pk=id)
        if collection.products.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "There are products related to this collectio, you can not delete it"
                },
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        else:
            collection.delete()
            return Response(status.HTTP_404_NOT_FOUND)


class OrderList(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # override get
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetail(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = "id"

# ----------------------------------------------------------------------------


# 4-[ViewSets]:-

# Implement an [Product - Reviews] API:    Viewsets to make nested query: between [Product:parent, Reviews:child - Customer:parent,Orders:Child]
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related("collection")
    serializer_class = ProductSerializers
    pagination_class = ProductPagination
    # Customer Generic Filter:
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # User General Filters Ruels:
    search_fields = ["title", "description"]  # ?
    ordering_fields = ["unit_price", "last_update"]
    # filterset_fields = ['collection_id','unit_price'] # here genelral ruels is not suitable for a field like unit_price, so we will create a custom filter

    # Customer filter
    filterset_class = ProductFilter

    # #Create a specific filter:
    # def get_queryset(self):
    #     queryset = Product.objects.all().select_related('collection')
    #     # collectoin_id = self.request.query_params['collectoin_id']
    #     collectoin_id = self.request.query_params.get('collectoin_id')

    #     if collectoin_id is not None:
    #         queryset = queryset.filter(collectoin_id = collectoin_id)

    #     return queryset

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs["pk"])
        if self.product.orders.count() > 0:  # type: ignore
            return Response(
                {"error": "you can't delete it as you have purhsed it"},
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


# Implement an [Customer - Order] API:
class CustomerViewSet(ModelViewSet):
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
            ]

    queryset = Customer.objects.all()
    serializer_class = CustomerSrializer
    pagination_class = CustomerPagination
    filterset_class = CustomerFilter

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['first_name']
    ordering_fields = ['id']


class OrderViewSet(ModelViewSet):
    class OrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ["id", "placed_at", "payment_status", "customer"]

        def create(self, validated_data):
            customer_id = self.context["customer_id"]
            return Review.objects.create(product_id=customer_id, **validated_data)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.kwargs["customer_pk"])

    def get_serializer_context(self):
        return {"customer_id": self.kwargs["customer_pk"]}


# Implement an [Cart - CartItem] API:
class CartViewSet(GenericViewSet,
                  CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"Message": "This item has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class CartItemViewSet(ModelViewSet):
    # queryset = CartItem.objects.all() # we don't want to retrieve all cart items we only retrieve items of the cart we get into
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')
# ----------

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count("products")).all()
    serializer_class = CollectionSerializers

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(self.queryset, pk=kwargs["pk"])

        if collection.products.count() > 0:  # type: ignore
            return Response(
                {
                    "error": "There are products related to this collectio, you can not delete it"
                },
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)
