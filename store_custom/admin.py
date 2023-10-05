from django.contrib import admin
from store.admin import ProductAdmin
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline
from store.models import Product




# ModelInline: Give a tag to an [generic] tagged item inline:
class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ["tag"]
    extra = 1


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

admin.site.unregister(Product)

admin.site.register(Product,CustomProductAdmin)
