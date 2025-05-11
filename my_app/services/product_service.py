from my_app.models.product import Product
from django.db import transaction
import logging

class ProductService:
    #store new products by batch
    @staticmethod
    def batch_upsert_products(param_product_list):
        existing_products_names = []
        failed_products_data = []
        #1. create list of Products (NOT save to DB yet)
        products_to_create = []
        for product in param_product_list:
            product = Product(
                    name=product['name'],
                    product_id=product['product_id']
                )
            products_to_create.append(product)
        #get all products from db to compare
        db_products = list(Product.objects.all())
        print(len(db_products))
        try:
            with transaction.atomic():
                Product.objects.bulk_create(
                        products_to_create,
                        update_conflicts=True,  # Key to enabling upsert (Do not create new record)
                        unique_fields=['name'],  # Specify the unique field(s)
                        update_fields=['product_id']
                    )
        except Exception as e:
            print(e)
            print(f"Failed upsert {len(param_product_list)} products. Transaction rolled back.")
        else:
            print(f"Successfully upsert {len(param_product_list)} products.")
        return len(param_product_list)
    #========== clear all data (only for testing)
    @staticmethod
    def clear_all():
        try:
            deleted_count, _ = Product.objects.all().delete()
            return deleted_count
        except Exception as e:
            print(f"Error deleting data from {Product.__name__}: {e}")
            return 0