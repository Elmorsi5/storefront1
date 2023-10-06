from . import views
from rest_framework_nested import routers
from django.urls import include, path

#ViewSetsURl:
#step1 - [General Step]
router = routers.DefaultRouter() 

#step2 - [General Step] parent router register - Each view set have it's own register 
router.register('products',views.ProductViewSet) # return --->[products-list]:products/ ,---> [products-detail]:products/<id>
router.register('collection-viewset',views.CollectionViewSet) 
router.register('reviews',views.ReviewViewSet,basename = 'reviews-list')

# step 3:[Optional for building Nested Routers]
#3.1:Select parent router and the prefix to it's prefix, which is here:router, 'products'
products_router = routers.NestedDefaultRouter(router,'products',lookup = 'product') 
#3.2: register the child router based on the parent:
products_router.register('reviews',views.ReviewViewSet,basename='product-reviews') #follow the parent with this child



urlpatterns = [
    path('customer/<int:id>',views.customer_detail),
    path('customers/',views.customer_list),
    path('products/',views.ProductList.as_view()),
    path('product/<int:id>',views.ProductDetail.as_view()), #<int:id> called converter
    path('collections/',views.CollectionList.as_view()), 
    path('collection/<int:pk>',views.CollectionDetail.as_view()), #<int:id> called converter
    path('orders/',views.OrderList.as_view()),
    path('order/<int:id>',views.OrderDetail.as_view()),
    path('reviews_list/',views.ReviewList.as_view()),

    
    # ViewSets Router
    path(r'',include(router.urls)),# router.urls map the viewsets that regiserin in:
    path(r'',include(products_router.urls)),
    ]