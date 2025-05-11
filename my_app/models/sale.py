from django.db import models
from django.db.models import UniqueConstraint

#Store sale info (dismissed fields that are not in requirements)
class Sale(models.Model):
    date = models.CharField(max_length=12) #same as in file DD/MM/YYYY
    order_id = models.IntegerField()      #Sale ID in the file (could be duplicated)
    product_id = models.IntegerField()  #Link to the table Product
    amount_sgd = models.FloatField()    #Total Paid w/ Payment Method
    # Add other sale-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['date', 'order_id', 'product_id'], name='unique_sale_record'),
    #     ]

    def __str__(self):
        return self.name