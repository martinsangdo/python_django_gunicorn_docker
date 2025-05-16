# from django.db import models
from mongoengine import *

#product details
class Product(Document):
    name = StringField(max_length=255, unique=True)
    price = DecimalField(max_digits=10, decimal_places=2, null=True)
    # color = models.CharField(max_length=16) #unknown property
    # size = models.IntegerField() #unknown property
    # Add other product-related fields
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name