"""
This module contains the base test class for the application.
"""

import logging
import unittest

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from ecom_app import create_app
from ecom_app.database import db
from ecom_app.models import Seller, Product, Order, Status


logging.basicConfig(filename='test_log.log',
                    filemode='a',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


class BaseTest(TestCase):
    """
    This class contains the base test class for the application
    """
    @staticmethod
    def populate_db():
        """
        This function populates the database with test data
        """
        logger.debug('Populating database')

        seller1 = Seller(name='Seller 1', email='seller1@example.com', phone='+380968102936',
                         password=generate_password_hash('seller1password', method='sha256'), is_admin=True)
        seller2 = Seller(name='Seller 2', email='seller2@example.com', phone='+380961238931',
                         password=generate_password_hash('seller2password', method='sha256'))
        product1 = Product(name='Product 1', description="Description 1", price=100, inventory=1, seller_id=1)
        product2 = Product(name='Product 2', description="Description 2", price=200, inventory=2, seller_id=1)
        product3 = Product(name='Product 3', description="Description 3", price=300, inventory=3, seller_id=2)
        product4 = Product(name='Product 4', description="Description 4", price=400, inventory=4, seller_id=2)
        order1 = Order(product_id=1, quantity=1, seller_id=1, customer_details='Customer details',
                       status=Status.in_progress)
        order2 = Order(product_id=2, quantity=2, seller_id=1, customer_details='Customer details',
                       status=Status.in_progress)
        order3 = Order(product_id=2, quantity=1, seller_id=1, customer_details='Customer details',
                       status=Status.complete)
        order4 = Order(product_id=3, quantity=3, seller_id=2, customer_details='Customer details',
                       status=Status.in_progress)
        order5 = Order(product_id=4, quantity=4, seller_id=2, customer_details='Customer details',
                       status=Status.in_progress)
        order6 = Order(product_id=4, quantity=1, seller_id=2, customer_details='Customer details',
                       status=Status.complete)

        db.session.add(seller1)
        db.session.add(seller2)
        db.session.add(product1)
        db.session.add(product2)
        db.session.add(product3)
        db.session.add(product4)
        db.session.add(order1)
        db.session.add(order2)
        db.session.add(order3)
        db.session.add(order4)
        db.session.add(order5)
        db.session.add(order6)
        db.session.commit()

    def create_app(self):
        """
        This function creates the flask application
        """
        logger.debug('Creating app')
        app = create_app(test_config={'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:', 'TESTING': True,
                                      'SECRET_KEY': 'test_key', 'WTF_CSRF_ENABLED': False})
        return app

    def setUp(self):
        """
        This function sets up the test environment
        """
        logger.debug('Setting up')
        self.app = self.create_app().test_client()
        db.create_all()
        self.populate_db()

    def tearDown(self):
        """
        This function tears down the test environment
        """
        logger.debug('Tearing down')
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
