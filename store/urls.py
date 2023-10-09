from . import views
from rest_framework_nested import routers
from django.urls import include, path

# ViewSetsURl:
router = routers.DefaultRouter()

router.register("products", views.ProductViewSet, basename="products")
router.register("reviews", views.ReviewViewSet, basename="reviews")
router.register("customers", views.CustomerViewSet)
router.register("orders", views.OrderViewSet, basename="orders")
router.register("carts", views.CartViewSet, basename="carts")
router.register("cart_items", views.CartItemViewSet, basename="cart_items")
router.register("collection-viewset", views.CollectionViewSet)

# 1-For building Nested Routers:
products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
customers_router = routers.NestedDefaultRouter(router, "customers", lookup="customer")
carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")

# 2-Register child router to the parent: ParntRouterURL/ChildRouterURL
# [Products has reviews 1.1]
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
# [Customer has orders]
customers_router.register("orders", views.OrderViewSet, basename="customer-orders")
# [Carts iclude orders]
carts_router.register("cart_items", views.CartItemViewSet, basename="cart-cartitems")


urlpatterns = [
    # path('customer/<int:id>',views.customer_detail),
    # path('customers/',views.customer_list),
    # path('products/',views.ProductList.as_view()),
    # path('product/<int:id>',views.ProductDetail.as_view()), #<int:id> called converter
    # path('collections/',views.CollectionList.as_view()),
    # path('collection/<int:pk>',views.CollectionDetail.as_view()), #<int:id> called converter
    # path('orders/',views.OrderList.as_view()),
    # path('order/<int:id>',views.OrderDetail.as_view()),
    # path('reviews_list/',views.ReviewList.as_view()),
    # ViewSets Router
    path(r"", include(router.urls)),  # router.urls map the viewsets that regiserin in:
    path(r"", include(products_router.urls)),
    path(r'',include(customers_router.urls)),
    path(r"", include(carts_router.urls)),
]
