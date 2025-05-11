from django.db import models

#product details
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # color = models.CharField(max_length=16) #unknown property
    # size = models.IntegerField() #unknown property
    # Add other product-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name