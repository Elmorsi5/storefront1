from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer,Product,OrderItem,Order,Collection,Cart,CartItem,Order
from django.db.models import Q
from django.db import connection, transaction
from django.db.models import Max,Value,Count 
# Create your views here.
def say_hello(request):
    # qs = Customer.objects.values_list('first_name','last_name')
    # qs = Customer.objects.values() #return list of dict
    # qs = Customer.objects.values() #return list of object instances

    # qs = Customer.objects.values_list('first_name') #return list of tubels
    # qs = Customer.objects.values_list('first_name',flat=True) #return list of tuble values only, not the whole tuple

    # qs = Customer.objects.annotate(last_order = Max("order"))
    # qs = Collection.objects.annotate(number_of_products = Count("product"))
    # qs = Customer.objects.annotate(num_of_orders=Count("order")).filter(num_of_orders__gt = 5)
    qs= Customer.objects.annotate(total = Count("order")).filter(~Q(total__gt = 0))
    # qs= Customer.objects.annotate(toatal_number_of_products_in_orders = Count("order"))


    return render(request,'hello.html',{'customers':qs})
    return True


def get_tagged_item(request):
    tagged_items = TaggedItem.tagged.get_tags_for(Product,1)
    return render(request,'get_tagged_item.html',{'items':tagged_items})    


def create_collection(request):
    collection = Collection()
    collection.title = "Video Games"
    collection.featured_product = None
    collection.save()

def update_collection(request):
    #best practice is to read the object then update it
    collection = Collection.objects.get(pk=1)
    collection.title = "Videos"
    collection.save()
    #collection.objects.filter(pk=1).update(title = 'videos)

def delete_collection(request):
    #best practice is to read the object then delete it
    collection = Collection.objects.get(pk=1)
    collection.delete()
    #collection.objects.filter(pk=1).delete()
    #collection.objects.filter(id__gt = 5).delete()

def create_cart(request):
    cart = Cart()
    cart.save()
    item1 = CartItem()
    item1.cart = cart
    item1.product = Product(id=1)
    item1.quantity = 1
    item1.save()

def update_cart(request):
    item = CartItem.objects.get(id=1)
    item.quantity = 2

def remove_cart(request):
    cart = Cart.objects.get(pk=1)
    cart.delete()
    

def create_order(request):
    #Transaction:
    with transaction.atomic():
        # order can't be done without having items in it.
        order = Order()
        order.customer = Customer(pk=1)
        order.save()

        item = OrderItem()
        item.order = order
        item.product = Product(pk=1)
        item.quantity = 5
        item.unit_price = OrderItem.objects.get(id=2).unit_price
        item.save()

# Writing queries using raw sql
def raw_sql(request):
    queryset = Product.objects.raw('SELECT * FROM store_product')
    #another way using cursor method #Task: search the difference between cursor and raw sql
    with connection.cursor() as cursor:
        cursor.callproc('get_customers',[1,2,'a']) # to avoide writing raw sql inside python code directly

    

    return render(request,'test.html',{'items':list(queryset)})    
