from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=36)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=16) #unknown property
    size = models.IntegerField() #unknown property
    # Add other product-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name