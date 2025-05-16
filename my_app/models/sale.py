# from django.db import models
# from django.db.models import UniqueConstraint
from mongoengine import *

#Store sale info (dismissed fields that are not in requirements)
class Sale(Document):
    date = DateField() #same as in file DD/MM/YYYY
    order_id = IntField()      #Sale ID in the file (could be duplicated)
    product_id = IntField()  #Link to the table Product
    amount_sgd = FloatField()    #Total Paid w/ Payment Method
    # Add other sale-related fields
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['date', 'order_id', 'product_id'], name='unique_sale_record'),
    #     ]

    def __str__(self):
        return str(self.date)