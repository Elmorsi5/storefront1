from . import views
from django.urls import path

urlpatterns = [
    path('products/',views.ProductList.as_view()),
    path('product/<int:id>',views.ProductDetail.as_view()), #<int:id> called converter
    path('collections/',views.CollectionList.as_view()), 
    path('collection/<int:pk>',views.CollectionDetail.as_view()), #<int:id> called converter
    path('customers/',views.customer_list),
    path('customer/<int:id>',views.customer_detail),
    path('orders/',views.OrderList.as_view()),
    path('order/<int:id>',views.OrderDetail.as_view()),

    ]