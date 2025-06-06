import csv
import pandas as pd

from my_app.models.sale import Sale
from .. import settings
from . import product_service
from django.db import transaction
from django.db.models import Sum, Avg

class SaleService:
    def read_csv(self):
        try:
            df = pd.read_csv(settings.FILE_PATH)
            return df
        except Exception as e:
            print(f"An error occurred while reading file: {e}")
        return None
    #========== Upsert new sales at once
    def batch_upsert_sales(self, df):
        sales_2_store = []
        for index, row in df.iterrows():
            #1. create list of Sales (NOT save to DB yet)
            sale = Sale(
                    date = row['date_yyyymmdd'],   #converted date
                    order_id = row['Sale ID'],
                    product_id = row['product_id'],
                    amount_sgd = row['Total Paid w/ Payment Method']
                )
            sales_2_store.append(sale)
        try:
            with transaction.atomic():
                #insert all
                Sale.objects.bulk_create(
                        sales_2_store,
                        update_conflicts=False,  # Key to enabling upsert (Do not create new record)
                        # unique_fields=['date', 'order_id', 'product_id' ],  # Specify the unique field(s)
                        # update_fields=['amount_sgd']
                    )
        except Exception as e:
            print(e)
            print(f"Failed upsert sales. Transaction rolled back.")
            return {'error': e}
        else:
            print(f"Successfully upsert sales.")
            return {'total': len(sales_2_store)}
    #========== Summarize the daily revenue
    #TODO optimize query
    def summarize_daily_revenue(self, df):
        try:
            # Group the DataFrame by 'date_yyyymmdd' and calculate the sum of 'Item Total' and the count of rows
            daily_summary = df.groupby('date_yyyymmdd').agg(
                Total_Item_Total=('Total Paid w/ Payment Method', 'sum'),  # Sum of 'Item Total' for each day
                Row_Count=('Sale ID', 'size')      # Count of rows for each day.  size() is like count() but includes NaN
            ).reset_index()  # Convert the grouped result back into a DataFrame
            return daily_summary
        except Exception as e:
            print(f"An error occurred: {e}")
        return pd.DataFrame() # Return empty DataFrame in case of error.
    #========== Batch store the daily revenue
    def store_daily_revenue(self):
        return
    #========== clear all data (ONLY for testing)
    def clear_all(self):
        try:
            deleted_count, _ = Sale.objects.all().delete()
            return deleted_count
        except Exception as e:
            print(f"Error deleting data from {Sale.__name__}: {e}")
            return 0
    #========== Get data from file & update into db
    #NOTE: The csv file is incorrect. Because 1 client can buy same product 
    def import_sales_from_file(self):
        df = self.read_csv()
        if df.empty:
            return {'error': settings.MESSAGES['ERR_FILE_CONTENT']}
        # Remove duplicate rows
        df = df.drop_duplicates()
        #create new column for the date YYYY-MM-DD
        df['date_yyyymmdd'] = pd.to_datetime(df['Sale Date'])
        df['date_yyyymmdd'] = df['date_yyyymmdd'].dt.strftime('%Y-%m-%d')
        #1. insert info into the table product
        product_names = df['Item name'].unique()
        result_products = product_service.ProductService.batch_upsert_products(product_names)
        if 'error' in result_products:
            return {'error': settings.MESSAGES['ERR_UPSERT_PRODUCTS']}
        product_map = result_products['product_name_map']
        #create new product_id column
        df['product_id'] = df['Item name'].map(product_map)
        #df.drop(df[df['Sale ID'] != 0].index, inplace=True)
        #df[df['Sale ID'] == x].copy()
        # daily_summary = self.summarize_daily_revenue(df)
        # print(daily_summary)
        #TODO 1: Sale ID 4126 has 2 same product names with different quantity
        # duplicate_rows_df = df[df.duplicated(subset=['Sale Date', 'Sale ID', 'Item name'], keep=False)]
        # print(duplicate_rows_df)
        #TODO 2: Why there are Sale ID = 1 in multiple days?
        #clear all sales because the file has invalid sale record
        self.clear_all()
        result_insert_sales = self.batch_upsert_sales(df)
        if 'error' in result_insert_sales:
            return {'error': settings.MESSAGES['ERR_UPSERT_SALES']}
        #return number of rows
        return {"imported_rows": result_insert_sales['total']}
    #========== Get metrics in date range
    def overall_metrics(self, start_date, end_date):
        sales_in_range = Sale.objects.filter(date__range=(start_date, end_date)).order_by('date')
        total_revenue_sgd = 0
        average_order_value_sgd = 0
        order_sale_map = {}  #key: order id, value: total amount sgd
        for sale in sales_in_range:
            total_revenue_sgd += sale.amount_sgd
            if sale.order_id in order_sale_map:
                order_revenue = order_sale_map[sale.order_id]
                order_revenue += sale.amount_sgd
                order_sale_map[sale.order_id] = order_revenue
            else:
                order_sale_map[sale.order_id] = sale.amount_sgd
        #
        if len(sales_in_range) > 0:
            total_orders = len(order_sale_map)
            average_order_value_sgd = total_revenue_sgd / total_orders
        #
        response_data = {
                "total_revenue_sgd": total_revenue_sgd,
                "average_order_value_sgd": average_order_value_sgd  #avg revenue of each order(sale)
        }
        return response_data
    #========== Get daily metrics
    def daily_metrics(self, start_date, end_date):
        sales_in_range = Sale.objects.filter(date__range=(start_date, end_date)).order_by('date')
        average_order_value_sgd = 0
        order_sale_map = {}  #key: date, value: total amount sgd
        for sale in sales_in_range:
            str_date = str(sale.date)
            if str_date in order_sale_map:
                order_revenue = order_sale_map[str_date]
                order_revenue += sale.amount_sgd
                order_sale_map[str_date] = order_revenue
            else:
                order_sale_map[str_date] = sale.amount_sgd
        #
        results = []
        for item in order_sale_map:
            results.append({
                'date': item,
                'revenue_sgd': order_sale_map[item]
            })
        return results