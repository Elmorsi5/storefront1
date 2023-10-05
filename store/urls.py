from . import views
from django.urls import path

urlpatterns = [
    path('products/',views.product_list),
    path('product/<int:id>',views.product_detail), #<int:id> called converter
    ]