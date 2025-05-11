from django.db import models
#Store sale info (dismissed fields that are not in requirements)
class Sale(models.Model):
    sale_date = models.CharField(max_length=12)
    order_id = models.IntegerField()      #Sale ID in the file (could be duplicated)
    product_id = models.CharField(max_length=36)  #Link to the table Product
    total_paid = models.FloatField()    #amount_sgd
    # Add other sale-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name