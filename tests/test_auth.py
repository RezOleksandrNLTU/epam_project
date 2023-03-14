"""
This module contains the tests for the auth blueprint
"""

from flask_login import login_user, current_user

from tests.conftest import BaseTest, logger
from ecom_app.models import Seller


class TestAuth(BaseTest):
    """
    This class contains the tests for the auth blueprint
    """

    def test_login(self):
        """
        This function tests the login function
        """
        logger.info('Testing login function')
        with self.client:
            response = self.client.post('/login', data=dict(email='seller1@example.com', password='invalid'),
                                        follow_redirects=True)
            self.assertFalse(current_user.is_authenticated)

            response = self.client.post('/login', data=dict(email='seller1@example.com', password='seller1password'),
                                        follow_redirects=True)
            self.assertTrue(current_user.is_authenticated)

    def test_logout(self):
        """
        This function tests the logout function
        """
        logger.info('Testing logout function')
        with self.client:
            login_user(Seller.query.all()[0])
            self.assertTrue(current_user.is_authenticated)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertFalse(current_user.is_authenticated)