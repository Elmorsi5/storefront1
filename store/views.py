from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers
from .models import Product
# Create your views here.

@api_view()
def product_list(rquest):
    queryset = Product.objects.all()
    serializer = ProductSerializers(queryset, many= True) #many =True: to tell the serializer to iterate over the queryset objects and convert it 
    return Response(serializer.data)

@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product,pk = id) #1- get the product object that we want to serialize
    serializer = ProductSerializers(product) #2- converr the specific fields to python dic and assgin it to  data variable- then django automatic render it to json under the hood when return the response
    serializer.data #this is the output: python dic -> automatic to JSNON
    return Response(serializer.data)
