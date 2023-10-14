from typing import Any
from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from tags.models import TaggedItem
from .models import Collection,Product,Customer,Order,OrderItem,Cart,CartItem
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
import datetime



#Custom Filters:-

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10','low') 
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt = 10) 


#Custom Filter by [today,last_week,last_month]
class DateFilter(admin.SimpleListFilter):
    title = "Date"
    parameter_name = 'Date'
    current_date = datetime.datetime.today()
    current_date_str= str(datetime.date.today())
    yesterday = str((current_date - datetime.timedelta(hours=24)).date())
    last_week = str((current_date - datetime.timedelta(days=7)).date())
    last_month = str((current_date - datetime.timedelta(weeks= 4)).date())

    filter_ranges = [current_date_str,yesterday,last_week,last_month]

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            (self.current_date_str,'today'),
            (self.yesterday,'yesterday'),
            (self.last_week,'last week'),
            (self.last_month,'last month')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        for filter_range in self.filter_ranges: 
            if filter_range == self.value():
                return queryset.filter(placed_at__date__gte = filter_range)



#Admin Panels:-

@admin.register(Product)    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','collection_title','inventory_status']
    search_fields = ['title']
    ordering = ['collection','title']
    autocomplete_fields = ['collection']  #Use it with the droplist to override the bad effect of having huge number of choices
    prepopulated_fields ={
        'slug':['title']
    }
    actions = ["clear_inventory"]
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]


    def collection_title(self,product):
        return product.collection.title

    #Adding computed columns:
    @admin.display(ordering='inventory')
    def inventory_status(self,product): #It call this method over every object and return opposite value
        if product.inventory<10:
            return 'Low'
        return 'Ok'
    
    # Create Custom Action
    def clear_inventory(self,request,queryset):
        updated_count = queryset.update(inventory = 0)
        self.message_user(request,f'{updated_count} products were successfully updated',messages.SUCCESS)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id','title','products_count']
    search_fields = ['title'] # which field to use when we search for a collection

    @admin.display(ordering='products_count')
    def products_count(self,collectoin):
        url = (reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection__id' : str(collectoin.id)
                }))
        return format_html('<a href="{}">{}</a>',url,collectoin.products_count)


    # for each collection object give me the count of the related procuts
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields =['user']
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']

    #override the base queryset using annotate to return the number of orders for each customer
    @admin.display(ordering='orders_count')
    def orders_count(self,customer):
        url = (reverse('admin:store_order_changelist')
               + "?"
               + urlencode({
                   'customer__id':str(customer.id)
               }))
        return format_html('<a href = "{}">{}</a>',url,customer.orders_count)
    

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders_count = Count('orders')
        )


#Add products to order inline:
class OrderItemInline(admin.TabularInline):  #Able to inherit from StackInline
    model = OrderItem
    autocomplete_fields = ['product']
    min_num = 1 #Must assign 1 order at least when creat an order
    max_num = 10  #Can't assign more than 10 products when create an order
    extra = 1 #Number of items in single bar - Default is 3

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id','placed_at','payment_status','customer']
    inlines = [OrderItemInline]
    actions = ['convert_pending']
    list_filter = ['payment_status',DateFilter]
    list_select_related = ['customer']
    search_fields = ['customer__first_name'] #with strings us
    date_hierarchy = 'placed_at'
    
    #Custom Action:
    def convert_pending(self,request,queryset):
       updated_count = queryset.update(payment_status = Order.PaymentStatus.PENDING)
       self.message_user(request,f'{updated_count} Order were successfully updated',messages.SUCCESS)
    


class CartItemInLine(admin.TabularInline):
    model = CartItem
    autocomplete_fields = ['product']
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['created_at']
    inlines = [CartItemInLine]




