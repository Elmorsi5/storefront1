from . import views
from django.urls import path

urlpatterns = [
    path('hello/',views.say_hello),
    path('get_tagged_item/',views.get_tagged_item )
]
