# here we create the customization of each appliatoin panel in the Admin Site App
from django.contrib import admin
from .models import Collection,Product,Customer,Order

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
    list_display = ['title']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name','last_name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','placed_at','payment_status']
    ordering = ['customer']

