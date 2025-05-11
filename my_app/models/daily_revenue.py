from django.db import models
#Store the daily renenue (We use this extra table for faster query. This table should be updated once we have new sale in a day)
class DailyRevenue(models.Model):
    sale_date = models.CharField(max_length=12) #YYYY-MM-DD -> we should make this index
    total_revenue_sgd = models.FloatField()
    average_order_value_sgd = models.FloatField()
    # Add other product-related fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name