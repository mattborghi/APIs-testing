from django.db import models

# Create your models here.

#  define a Model – the layer between Django and the database.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)