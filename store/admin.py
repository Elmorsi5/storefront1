# here we create the customization of each appliatoin panel in the Admin Site App
from django.contrib import admin
from .models import Collection , Product

# Register your models here.

admin.site.register(Collection)
admin.site.register(Product)


