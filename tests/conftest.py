import unittest

from flask_testing import TestCase

from ecom_app import create_app


class BaseTest(TestCase):
    def create_app(self):
        app = create_app()
        return app


if __name__ == '__main__':
    unittest.main()
