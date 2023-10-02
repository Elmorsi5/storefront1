from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer,Product,OrderItem,Order,Collection
from django.db.models import Q
from django.db.models import Max,Value,Count 
# Create your views here.
def say_hello(request):
    # qs = Customer.objects.values_list('first_name','last_name')
    # qs = Customer.objects.values() #return list of dict
    # qs = Customer.objects.values() #return list of object instances

    # qs = Customer.objects.values_list('first_name') #return list of tubels
    # qs = Customer.objects.values_list('first_name',flat=True) #return list of values 

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
    collection = Collection.objects.get(pk=1)
    collection.title = "Videos"
    collection.save()
    #collection.objects.filter(pk=1).update(title = 'videos)
