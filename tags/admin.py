from django.contrib import admin
from .models import Tag,TaggedItem
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['tag']
    search_fields = ['tag']


@admin.register(TaggedItem)
class TaggedIem(admin.ModelAdmin):
    list_display = ['tag','content_type','object_id']
    search_fields = ['tag']
    autocomplete_fields = ['tag']
    list_filter = ['tag','content_type']
