"""
This module contains the tests for the seller service functions
"""

from tests.conftest import BaseTest, logger
from werkzeug.security import generate_password_hash, check_password_hash

from ecom_app.service.seller_service import *


class TestSellerService(BaseTest):
    """
    This class contains the tests for the seller service functions
    """
    def test_get_sellers(self):
        """
        This function tests the get_sellers function
        """
        logger.info('Testing get_sellers function')
        sellers = get_sellers()
        self.assertEqual(len(sellers), 2)
        self.assertTrue(isinstance(sellers[0], Seller))
        self.assertTrue(isinstance(sellers[1], Seller))

    def test_get_seller_by_id(self):
        """
        This function tests the get_seller_by_id function
        """
        logger.info('Testing get_seller_by_id function')
        seller = get_seller_by_id(1)
        self.assertEqual(seller.id, 1)

    def test_get_seller_by_email(self):
        """
        This function tests the get_seller_by_email function
        """
        logger.info('Testing get_seller_by_email function')
        seller = get_seller_by_email('seller1@example.com')
        self.assertEqual(seller.email, 'seller1@example.com')

    def test_create_seller(self):
        """
        This function tests the create_seller function
        """
        logger.info('Testing create_seller function')
        seller = create_seller(name='Seller 3', email='seller3@example.com', phone='1234567890', password='password',
                               is_admin=False)
        self.assertTrue(isinstance(seller, Seller))
        self.assertTrue(isinstance(Seller.query.filter_by(name='Seller 3').first(), Seller))

    def test_update_seller(self):
        """
        This function tests the update_seller function
        """
        logger.info('Testing update_seller function')
        updated_name = 'Seller 2 Updated'
        updated_email = 'seller2upd@wxample.com'
        updated_phone = '0987654321'
        updated_password = 'password'
        updated_is_admin = True

        seller = get_seller_by_id(2)

        updated_seller = update_seller(seller_id=2)

        self.assertEqual(updated_seller, seller)

        self.assertTrue(isinstance(seller, Seller))
        self.assertNotEqual(seller.name, updated_name)
        self.assertNotEqual(seller.email, updated_email)
        self.assertNotEqual(seller.phone, updated_phone)
        self.assertFalse(check_password_hash(seller.password, updated_password))
        self.assertNotEqual(updated_is_admin, seller.is_admin)

        update_seller(seller_id=2, name=updated_name, email=updated_email, phone=updated_phone,
                      password=generate_password_hash(updated_password, method='sha256'), is_admin=updated_is_admin)

        seller = get_seller_by_id(2)

        self.assertTrue(isinstance(seller, Seller))
        self.assertEqual(seller.name, updated_name)
        self.assertEqual(seller.email, updated_email)
        self.assertEqual(seller.phone, updated_phone)
        self.assertTrue(check_password_hash(seller.password, updated_password))
        self.assertEqual(seller.is_admin, updated_is_admin)

        self.assertFalse(update_seller(seller_id=-1))

    def test_delete_seller(self):
        """
        This function tests the delete_seller function
        """
        logger.info('Testing delete_seller function')

        seller = create_seller(name='Seller 3', email='seller3@example.com', phone='1234567890', password='password',
                               is_admin=False)

        sellers = get_sellers()
        self.assertEqual(len(sellers), 3)

        result = delete_seller(seller_id=3)
        self.assertTrue(result)

        sellers = get_sellers()
        self.assertEqual(len(sellers), 2)
        self.assertTrue(seller not in sellers)

        self.assertEqual(Seller.query.filter_by(id=3).first(), None)

        self.assertFalse(delete_seller(seller_id=-1))
