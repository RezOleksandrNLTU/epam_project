"""
This module contains the tests for the views
"""

from flask_login import login_user, current_user

from tests.conftest import BaseTest, logger
from ecom_app.models import Seller
from ecom_app.views import sellers, products, orders


class TestViews(BaseTest):
    """
    This class contains the tests for the views
    """
    def test_sellers_views(self):
        """
        This function tests the sellers views
        """
        logger.info('Testing sellers views')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/edit_profile')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/sellers')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/sellers/edit/2')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/sellers/add')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/sellers/invalid')
            self.assertEqual(response.status_code, 404)

        with self.client:
            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/profile')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/edit_profile')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/sellers')
            self.assertEqual(response.status_code, 403)

            response = self.client.get('/sellers/edit/2')
            self.assertEqual(response.status_code, 403)

            response = self.client.get('/sellers/add')
            self.assertEqual(response.status_code, 403)

            response = self.client.get('/sellers/invalid')
            self.assertEqual(response.status_code, 404)

    def test_products_views(self):
        """
        This function tests the products views
        """
        logger.info('Testing sellers views')
        with self.client:
            login_user(Seller.query.all()[0])
            response = self.client.get('/products')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/products/add')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/products/edit/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/products/invalid')
            self.assertEqual(response.status_code, 404)

            response = self.client.get('/products/edit/invalid')
            self.assertEqual(response.status_code, 404)

    def test_orders_views(self):
        """
        This function tests the orders views
        """
        logger.info('Testing orders views')
        with self.client:
            login_user(Seller.query.all()[0])
            response = self.client.get('/orders')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('orders/add')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('orders/edit/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('orders/invalid')
            self.assertEqual(response.status_code, 404)

            response = self.client.get('orders/edit/invalid')
            self.assertEqual(response.status_code, 404)


