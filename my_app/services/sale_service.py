import csv
import pandas as pd
from .. import settings
from . import product_service

def read_csv():
    try:
        df = pd.read_csv(settings.FILE_PATH)
        return df
    except Exception as e:
        print(f"An error occurred while reading file: {e}")
    return None

def import_sales_from_file():
    df = read_csv()
    if df.empty:
        return {'error': settings.MESSAGES['ERR_FILE_CONTENT']}
    #1. insert info into the table product
    product_names = df['Item name'].unique()
    product_map = {} #key = product name, value = json of properties
    #generate product id
    products_to_create = []
    for product_name in product_names:
        product_map[product_name] = {
            'name': product_name,
            'product_id': settings.get_random_uuid()
            #size, color, etc. are not required in the doc
        }
        products_to_create.append(product_map[product_name])
    #print(product_map)
    #product_service.ProductService.clear_all()
    product_service.ProductService.batch_upsert_products(products_to_create)

    #for row in file_rows:

    #1.4 sale
    sale_map = {}   #key=uuid, value=json of properties

    #return number of rows
    return {}