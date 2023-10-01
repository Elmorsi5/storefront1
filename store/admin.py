# here we create the customization of each appliatoin panel in the Admin Site App
from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from .models import Collection,Product,Customer,Order,OrderItem
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode

# The original way to add model in the admin site and then applay it's customization which in it's ModelAdmin
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['title']
# admin.site.register(Product,ProductAdmin)

# Register your models here.


# Custom Filters
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
        
@admin.register(Product)    # here we are saying that Productadmin is the AdminModel of the Product model - register func take the model to register and applay what in it's modeladmin
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title']
    autocomplete_fields = ['collection']  # use it with the droplist to override the bad effect of having huge number of choices
    prepopulated_fields ={
        'slug':['title']
    }
    actions = ["clear_inventory"]
    list_display = ['title','unit_price','collection_title','inventory_status']
    list_editable = ['unit_price']
    ordering = ['collection','title']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    def collection_title(self,product):
        return product.collection.title

    # Adding computed columns
    @admin.display(ordering='inventory') # to order before applying the method
    def inventory_status(self,product): # it call this method over every object and retrun it's value in each iteration.
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
            products_count = Count('product')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']
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
            orders_count = Count('order')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1 # Must have at least one item per order
    max_num = 10  # Can't have more than 10 items per order
    model = OrderItem
    extra = 1 #Number of items in single bar- to change the default form 3 to 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id','placed_at','payment_status','customer']





