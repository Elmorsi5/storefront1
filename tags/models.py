from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=255)

#This enable us to use it (generic) with any project in the future because it'n not related to other projects
class TaggedItem(models.Model):
    tag = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.IntegerField()
    content_object = GenericForeignKey()
