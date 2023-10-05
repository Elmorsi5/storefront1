from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers
from .models import Product
# Create your views here.

@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializers(queryset, many= True) #many =True: to tell the serializer to iterate over the queryset objects and convert it 
        # return Response(serializer.data)
        return Response('ok')
    elif request.method == 'POST':
        serializer = ProductSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product,pk = id) #1- get the product object that we want to serialize
    if request.method == 'GET':
        serializer = ProductSerializers(product) #2- converr the specific fields to python dic and assgin it to  data variable- then django automatic render it to json under the hood when return the response
        serializer.data #this is the output: python dic -> automatic to JSNON
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializers(product,data = request.data) #we provide a product instanc to update the product by the data we serialize
        serializer.is_valid(raise_exception=True)
        serializer.save() #it call update method by defult
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count()>0: # type: ignore
            return Response({'error':"You have purched it "},status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status.HTTP_404_NOT_FOUND)


    


