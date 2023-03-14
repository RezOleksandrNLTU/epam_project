"""
This module contains the tests for the SellerAPI and SellersAPI RESTful resources
"""

from flask_login import login_user

from tests.conftest import BaseTest, logger
from ecom_app.models import Seller


class TestSellersAPI(BaseTest):
    """
    This class contains the tests for the SellersAPI RESTful resource
    """

    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/sellers')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 2)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/sellers')
            self.assertEqual(response.status_code, 403)

    def test_post(self):
        """
        This function tests the post method
        """
        logger.info('Testing post method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.post('/api/sellers', json={}, follow_redirects=True)

            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/sellers', follow_redirects=True, json={
                'name': '',
                'email': 'wrong_email',
                'phone': 'wrong_phone',
                'password': '123',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/sellers', follow_redirects=True, json={
                'name': 'test',
                'email': 'test@example.com',
                'phone': '+380960198274',
                'password': 'Strong_Password123',
            })

            self.assertEqual(response.status_code, 200)

            response = self.client.post('/api/sellers', follow_redirects=True, json={
                'name': 'test',
                'email': 'test@example.com',
                'phone': '+380111111111',
                'password': 'Strong_Password123',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.post('/api/sellers', follow_redirects=True, json={
                'name': 'test',
                'email': 'test@example.com',
                'phone': '38011111',
                'password': 'Strong_Password123',
            })
            self.assertEqual(response.status_code, 400)

            seller = Seller.query.filter_by(name='test').first()
            self.assertIsNotNone(seller)

            login_user(Seller.query.filter_by(is_admin=False).first())

            response = self.client.post('/api/sellers', follow_redirects=True)
            self.assertEqual(response.status_code, 403)


class TestSellerAPI(BaseTest):
    """
    This class contains the tests for the SellerAPI RESTful resource
    """
    def test_get(self):
        """
        This function tests the get method
        """
        logger.info('Testing get method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.get('/api/seller/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'Seller 1')

            response = self.client.get('/api/seller')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['name'], 'Seller 1')

            response = self.client.get('/api/seller/10')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.get('/api/seller/1')
            self.assertEqual(response.status_code, 403)

    def test_put(self):
        """
        This function tests the put method
        """
        logger.info('Testing put method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.put('/api/seller/1', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/seller', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/seller/10', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 404)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'name': 'test',
                'email': 'test@example.com',
                'phone': '+380964726931',
                'password': 'Strong_Password123',
            })
            self.assertEqual(response.status_code, 200)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'name': '',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'email': 'wrong_email',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'phone': '38011111',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'phone': '+380111111111',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'password': '123',
            })
            self.assertEqual(response.status_code, 400)

            response = self.client.put('/api/seller/1', follow_redirects=True, json={
                'password': 'forbidden_password#$%^&*()',
            })
            self.assertEqual(response.status_code, 400)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.put('/api/seller/1', json={}, follow_redirects=True)
            self.assertEqual(response.status_code, 403)

    def test_delete(self):
        """
        This function tests the delete method
        """
        logger.info('Testing delete method')
        with self.client:
            login_user(Seller.query.filter_by(is_admin=True).first())
            response = self.client.delete('/api/seller/1')
            self.assertEqual(response.status_code, 200)

            response = self.client.delete('/api/seller')
            self.assertEqual(response.status_code, 404)

            response = self.client.delete('/api/seller/10')
            self.assertEqual(response.status_code, 404)

            login_user(Seller.query.filter_by(is_admin=False).first())
            response = self.client.delete('/api/seller/2')
            self.assertEqual(response.status_code, 403)