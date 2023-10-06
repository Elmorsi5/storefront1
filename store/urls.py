from . import views
from django.urls import path

urlpatterns = [
    path('products/',views.product_list),
    path('product/<int:id>',views.product_detail), #<int:id> called converter
    path('collections/',views.collectoin_list), 
    path('collection/<int:id>',views.collection_detail), #<int:id> called converter
    path('customers/',views.customer_list),
    path('customer/<int:id>',views.customer_detail),
    path('orders/',views.order_list),
    # path('order/<int:id>',views.order_detail),


    ]