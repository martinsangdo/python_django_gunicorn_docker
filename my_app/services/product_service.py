from my_app.models.product import Product
from django.db import transaction
import logging

class ProductService:
    #store new products by batch
    @staticmethod
    def batch_upsert_products(products_data):
        products_to_create = []
        existing_products_names = []
        failed_products_data = []

        for product_data in products_data:
            existing_products_names.append(product_data['name'])
            try:
                # Create Product instances.  Important:  Do NOT save them yet.
                product = Product(
                    product_id=
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    # Add other fields as necessary
                )
                products_to_create.append(product)
            except ValueError as e:
                logger.error(f"Invalid data for product: {product_data}. Error: {e}")
                failed_products_data.append(product_data)  # Collect failed data
                products_to_create = [p for p in products_to_create if p.name != product_data['name']] # remove the invalid product.
        #begin saving to db
        try:
            with transaction.atomic():
                # Get existing products
                existing_products = list(Product.objects.filter(name__in=existing_products_names))
                existing_product_name_set = set()
                for existing_product in existing_products:
                    existing_product_name_set.add(existing_product.name)

                # Filter out existing products
                products_to_create = [product for product in products_to_create if product.name not in existing_product_name_set]

                # Bulk Create
                if products_to_create:
                    Product.objects.bulk_create(
                        products_to_create,
                        update_conflicts=True,  # Key to enabling upsert
                        unique_fields=['name'],  # Specify the unique field(s)
                        update_fields=['description', 'price'],  # Fields to update if a conflict occurs
                    )
                logger.info(f"Successfully upserted {len(products_data)} products.")
                failed_products = []
                for failed_product_data in failed_products_data:
                    failed_product = Product(
                        name=failed_product_data['name'],
                        description=failed_product_data['description'],
                        price=failed_product_data['price'],
                    )
                    failed_products.append(failed_product)
                return failed_products
        except IntegrityError as e:
            logger.error(f"IntegrityError during batch upsert: {e}")
            # Handle the error appropriately (e.g., log, raise, or return an error)
            return []
        except Exception as e:
            logger.error(f"Unexpected error during batch upsert: {e}")
            return []

    @staticmethod
    def get_product_by_id(product_id):
        try:
            return Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return None