"""
This module contains the tests for the ProductAPI and ProductsAPI RESTful resources
"""

from flask_login import login_user

from tests.conftest import BaseTest, logger
from ecom_app.models import Seller, Product


class TestProductsAPI(BaseTest):
    """
    This class contains the tests for the ProductsAPI RESTful resource
    """
    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/products')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 4)

            response = self.client.get('/api/products', query_string={
                'inventory_from': 2,
                'inventory_to': 3,
                'ordered_from': 2,
                'ordered_to': 3,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 2)

            response = self.client.get('/api/products', query_string={
                'inventory_from': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'inventory_from': -1,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'inventory_to': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'inventory_to': -1,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'ordered_from': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'ordered_from': -1,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'ordered_to': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.get('/api/products', query_string={
                'ordered_to': -1,
            })
            self.assertEqual(response.status_code, 400)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/products')
            self.assertEqual(response.status_code, 200)

            self.assertEqual(len(response.json), 2)
            response = self.client.get('/api/products', query_string={
                'inventory_from': 2,
                'inventory_to': 3,
                'ordered_from': 2,
                'ordered_to': 3,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 1)

    def test_post(self):
        """
        This function tests the post method
        """
        logger.info('Testing post method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.post('/api/products', json={}, follow_redirects=True)

            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'name': '',
                'description': 'toolong' * 100,
                'price': 'wrong_price',
                'inventory': 'wrong_inventory',
                'seller_id': 'wrong_seller_id',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'name': '',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'description': 'toolong' * 100,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'price': 0,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'inventory': -1,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/products', follow_redirects=True, json={
                'name': 'test',
                'description': 'test',
                'price': 10,
                'inventory': 10,
                'seller_id': 1,
            })

            self.assertEqual(response.status_code, 200)


class TestProductAPI(BaseTest):
    """
    This class contains the tests for the ProductAPI RESTful resource
    """
    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/product/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/api/product/100')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/product/3')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/api/product/1')
            self.assertEqual(response.status_code, 403)

    def test_put(self):
        """
        This function tests the put method
        """
        logger.info('Testing put method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.put('/api/product/1', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/product/100', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 404)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'name': '',
                'description': 'toolong' * 100,
                'price': 'wrong_price',
                'inventory': 'wrong_inventory',
                'seller_id': 'wrong_seller_id',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'name': '',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'description': 'toolong' * 100,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'price': 0,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'price': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'inventory': -1,
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'inventory': 'a',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'name': 'test',
                'description': 'test',
                'price': 10,
                'inventory': 10,
                'seller_id': 1,
            })
            self.assertEqual(response.status_code, 200)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.put('/api/product/1', follow_redirects=True, json={
                'name': 'test',
                'description': 'test',
                'price': 10,
                'inventory': 10,
                'seller_id': 2,
            })
            self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """
        This function tests the delete method
        """
        logger.info('Testing delete method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.delete('/api/product/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.delete('/api/product/100')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.delete('/api/product/2')
            self.assertEqual(response.status_code, 403)
