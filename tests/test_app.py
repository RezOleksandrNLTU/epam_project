"""
This module contains the tests for app creation
"""

from flask import Flask


from tests.conftest import BaseTest, logger
from ecom_app import create_app
from ecom_app.models import Seller


class TestApp(BaseTest):
    """
    This class contains the tests for app creation
    """
    def test_app(self):
        """
        This function tests the app
        """
        app = create_app()
        self.assertTrue(isinstance(app, Flask))
        self.assertTrue(app.config['SECRET_KEY'] is not None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] is not None)

    def test_cli(self):
        """
        This function tests custom commands
        """

        app = create_app()
        runner = app.test_cli_runner()

        result = runner.invoke(app.cli.commands['create_admin'], ['admin', 'admin@admin.com', '+380961234567', 'admin'])
        self.assertIn('Admin created successfully', result.output)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(Seller.query.filter_by(name='admin').first() is not None)
