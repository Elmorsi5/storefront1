from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    OrderSerializer,
    ProductSerializers,
    CollectionSerializers,
    CustomerSrializer,
)
from .models import Product, Collection, Customer, Order
from django.db.models import Count


# Create your views here.
#1-Function Based
#2-Class Based APIView 
#3-mixins - generic APIViews
#4-Viewset

#1-Using [Function Based View] [manually handle http methods and manually write the functionsto : [list- create - update - Delete] ]
@api_view(["GET", "POST"])
def customer_list(request):
    if request.method == "GET":
        queryset = Customer.objects.annotate(orders_count=Count("orders")).all()
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
#---------------------------------------------------

#2- Using [Class APIView] Class [no more of (if conditions) to handle http methods ]
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
# ---------------------------------------------------

#3- Using [GenericAPIView] [built in function do work,only provide unique(queryset-serializer_class -lookup_field) and Customize built in function if need]
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializers
    
    def get_serializer_context(self):
        return {'request':self.request}


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializers

    def delete(self,request,id):
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
#-----------------------------------------------------

#4- Using [ViewSets] [do all in one and override what you want to edit]
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializers
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(self.queryset, pk=id)

        if collection.products.count() > 0: # type: ignore
            return Response(
                {
                    "error": "There are products related to this collectio, you can not delete it"
                },
                status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class OrderList(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get(self,request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class OrderDetail(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'



