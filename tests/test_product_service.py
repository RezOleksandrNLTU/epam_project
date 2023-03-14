"""
This module contains the tests for the product service functions
"""

from tests.conftest import BaseTest, logger

from ecom_app.service.product_service import *


class TestService(BaseTest):
    """
    This class contains the tests for the product functions
    """
    def test_get_products(self):
        """
        This function tests the get_products function
        """
        logger.info('Testing get_products function')
        products = get_products()
        self.assertEqual(len(products), 4)
        self.assertTrue(all(isinstance(product, Product) for product in products))

    def test_get_products_filtered(self):
        """
        This function tests the get_products_filtered function
        """
        logger.info('Testing get_products_filtered function')
        products = get_products_filtered(None, None, None, None)
        self.assertEqual(len(products), 4)

        products = get_products_filtered(2, 3, 2, 3)

        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 2)
        self.assertTrue(products[1].id == 3)

    def test_get_product_by_id(self):
        """
        This function tests the get_product_by_id function
        """
        logger.info('Testing get_product_by_id function')
        product = get_product_by_id(1)
        self.assertEqual(product.id, 1)

    def test_get_product_by_name(self):
        """
        This function tests the get_product_by_name function
        """
        logger.info('Testing get_product_by_name function')
        product = get_product_by_name('Product 1')
        self.assertEqual(product.name, 'Product 1')

    def test_get_products_by_seller(self):
        """
        This function tests the get_products_by_seller function
        """
        logger.info('Testing get_products_by_seller function')
        products = get_products_by_seller(1)
        self.assertEqual(len(products), 2)
        self.assertTrue(all(product.seller_id == 1 for product in products))

    def test_get_products_by_seller_filtered(self):
        """
        This function tests the get_products_by_seller_filtered function
        """
        logger.info('Testing get_products_by_seller_filtered function')
        products = get_products_by_seller_filtered(1, None, None, None, None)
        self.assertEqual(len(products), 2)
        self.assertTrue(all(product.seller_id == 1 for product in products))

        products = get_products_by_seller_filtered(1, 2, 3, 2, 3)

        self.assertEqual(len(products), 1)
        self.assertTrue(products[0].id == 2)

    def test_filter_products_by_inventory(self):
        """
        This function tests the filter_products_by_inventory function
        """
        logger.info('Testing filter_products_by_inventory function')
        products_query = Product.query

        products = filter_products_by_inventory(products_query, 1, 2).all()
        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 1)
        self.assertTrue(products[1].id == 2)

        products = filter_products_by_inventory(products_query, 3, None).all()

        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 3)
        self.assertTrue(products[1].id == 4)

        products = filter_products_by_inventory(products_query, None, 2).all()
        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 1)
        self.assertTrue(products[1].id == 2)

        products = filter_products_by_inventory(products_query, None, None)
        self.assertEqual(products_query, products)

    def test_filter_products_by_ordered(self):
        """
        This function tests the filter_products_by_ordered function
        """
        logger.info('Testing filter_products_by_ordered function')
        products_query = Product.query

        products = filter_products_by_ordered(products_query, 1, 2).all()
        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 1)
        self.assertTrue(products[1].id == 2)

        products = filter_products_by_ordered(products_query, 3, None).all()

        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 3)
        self.assertTrue(products[1].id == 4)

        products = filter_products_by_ordered(products_query, None, 2).all()
        self.assertEqual(len(products), 2)
        self.assertTrue(products[0].id == 1)
        self.assertTrue(products[1].id == 2)

        products = filter_products_by_ordered(products_query, None, None)
        self.assertEqual(products_query, products)

    def test_create_product(self):
        """
        This function tests the create_product function
        """
        logger.info('Testing create_product function')
        product = create_product('Product 5', 'Description 5', 5.0, 5, 1)
        self.assertEqual(product.name, 'Product 5')
        self.assertEqual(product.description, 'Description 5')
        self.assertEqual(product.price, 5.0)
        self.assertEqual(product.inventory, 5)
        self.assertEqual(product.seller_id, 1)

    def test_update_product(self):
        """
        This function tests the update_product function
        """
        logger.info('Testing update_product function')
        updated_name = 'Product 1 Updated'
        updated_description = 'Description 1 Updated'
        updated_price = 1000.0
        updated_inventory = 10
        updated_seller_id = 2

        product = get_product_by_id(1)

        updated_product = update_product(1)

        self.assertEqual(product, updated_product)

        updated_product = update_product(1, updated_name, updated_description, updated_price, updated_inventory, updated_seller_id)

        self.assertEqual(updated_product.name, updated_name)
        self.assertEqual(updated_product.description, updated_description)
        self.assertEqual(updated_product.price, updated_price)
        self.assertEqual(updated_product.inventory, updated_inventory)
        self.assertEqual(updated_product.seller_id, updated_seller_id)

        self.assertFalse(update_product(product_id=-1))

    def test_delete_product(self):
        """
        This function tests the delete_product function
        """
        logger.info('Testing delete_product function')
        product = get_product_by_id(1)
        products = get_products()
        self.assertEqual(len(products), 4)

        result = delete_product(product.id)

        self.assertTrue(result)
        self.assertFalse(delete_product(product.id))

        products = get_products()
        self.assertEqual(len(products), 3)
        self.assertTrue(product not in products)
