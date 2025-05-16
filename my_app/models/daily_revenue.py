# from django.db import models
from mongoengine import *

#Store the daily renenue (We use this extra table for faster query. This table should be updated once we have new sale in a day)
class DailyRevenue(Document):
    date = StringField(max_length=12) #YYYY-MM-DD -> we should make this index
    total_revenue_sgd = FloatField() #all revenue in a day
    sale_num = IntField()   #total of orders in a day
    # Add other product-related fields
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name