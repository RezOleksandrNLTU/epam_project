"""
This module contains the tests for the OrderAPI and OrdersAPI RESTful resources
"""

from flask_login import login_user

from tests.conftest import BaseTest, logger
from ecom_app.models import Seller, Order


class TestOrdersAPI(BaseTest):
    """
    This class contains the tests for the OrdersAPI RESTful resource
    """
    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/orders')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 6)

            response = self.client.get('/api/orders', query_string={
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 4)

            response = self.client.get('/api/orders', query_string={
                'status': 'a',
            })
            self.assertEqual(response.status_code, 400)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/orders')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 3)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/orders', query_string={
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 2)

    def test_post(self):
        """
        This function tests the post method
        """
        logger.info('Testing post method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.post('/api/orders', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 1,
                'quantity': 1,
                'customer_details': 'test',
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 'a',
                'quantity': 1,
                'customer_details': 'test',
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 1,
                'quantity': 'a',
                'customer_details': 'test',
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 1,
                'quantity': 0,
                'customer_details': 'test',
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 10,
                'quantity': 1,
                'customer_details': 'test',
                'status': 'In progress',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/orders', follow_redirects=True, json={
                'product_id': 1,
                'quantity': 1,
                'customer_details': 'test',
                'status': 'a',
            })
            self.assertEqual(response.status_code, 400)


class TestOrderAPI(BaseTest):
    """
    This class contains the tests for the OrderAPI RESTful resource
    """
    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/order/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['id'], 1)

            response = self.client.get('/api/order/10')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/order/1')
            self.assertEqual(response.status_code, 403)

            response = self.client.get('/api/order/10')
            self.assertEqual(response.status_code, 404)

    def test_put(self):
        """
        This function tests the put method
        """
        logger.info('Testing put method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.put('/api/order/1', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/order/10', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 404)

            response = self.client.put('/api/order/1', json={
                'product': 2,
                'quantity': 2,
                'customer_details': 'test',
                'status': 'Complete',
            })
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/order/1', json={
                'product': 10,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/order/1', json={
                'quantity': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/order/1', json={
                'quantity': 0,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/order/1', json={
                'customer_details': 'wrong' * 100,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/order/1', json={
                'status': 'a',
            })
            self.assertEqual(response.status_code, 400)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.put('/api/order/1', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """
        This function tests the delete method
        """
        logger.info('Testing delete method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.delete('/api/order/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.delete('/api/order/10')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.delete('/api/order/2')
            self.assertEqual(response.status_code, 403)
