# here we create the customization of each appliatoin panel in the Admin Site App
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Collection,Product,Customer,Order
from django.db.models import Count

# The original way to add model in the admin site and then applay it's customization which in it's ModelAdmin
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title']
# admin.site.register(Product,ProductAdmin)

# Register your models here.

@admin.register(Product)    # here we are saying that Productadmin is the AdminModel of the Product model - register func take the model to register and applay what in it's modeladmin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','collection_title','inventory_status']
    list_editable = ['unit_price']
    ordering = ['collection','title']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self,product):
        return product.collection.title

    # Adding computed columns
    @admin.display(ordering='inventory') # to order before applying the method
    def inventory_status(self,product): # it call this method over every object and retrun it's value in each iteration.
        if product.inventory<10:
            return 'Low'
        return 'Ok'
    
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']

    @admin.display(ordering='products_count')
    def products_count(self,collectoin):
        return collectoin.products_count
    # for each collection object give me the count of the related procuts
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )



@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']

    @admin.register(Order)
    class OrderAdmin(admin.ModelAdmin):
        list_display = ['id','placed_at','payment_status','customer']
    
    #override the base queryset using annotate to return the number of orders for each customer
    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        return customer.orders_count
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )




