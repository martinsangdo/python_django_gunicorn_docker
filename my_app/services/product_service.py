from my_app.models.product import Product
from django.db import transaction
import logging

class ProductService:
    #store new products by batch
    @staticmethod
    def batch_upsert_products(param_product_names):
        #1. create list of Products (NOT save to DB yet)
        products_to_create = []
        for product_name in param_product_names:
            product = Product(
                    name = product_name
                )
            products_to_create.append(product)
        try:
            with transaction.atomic():
                Product.objects.bulk_create(
                        products_to_create,
                        update_conflicts=True,  # Key to enabling upsert (Do not create new record)
                        unique_fields=['name'],  # Specify the unique field(s)
                        update_fields=['price']
                    )
        except Exception as e:
            print(e)
            print(f"Failed upsert {len(param_product_names)} products. Transaction rolled back.")
            return {'error': e}
        else:
            print(f"Successfully upsert {len(param_product_names)} products.")
            #get all products in db
            db_products = Product.objects.all().values('id', 'name')
            product_name_map = {}   #key: name, value: id
            #for index, product in enumerate(Product.objects.all()):
            for product in db_products:
                product_name_map[product['name']] = product['id']
            return {'product_name_map': product_name_map}
    #========== clear all data (ONLY for testing)
    @staticmethod
    def clear_all():
        try:
            deleted_count, _ = Product.objects.all().delete()
            return deleted_count
        except Exception as e:
            print(f"Error deleting data from {Product.__name__}: {e}")
            return 0