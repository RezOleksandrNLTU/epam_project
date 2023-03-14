"""
This module contains the tests for the order service functions
"""

from tests.conftest import BaseTest, logger

from ecom_app.service.order_service import *


class TestOrderService(BaseTest):
    """
    This class contains the tests for the order service functions
    """
    def test_get_orders(self):
        """
        This function tests the get_orders function
        """
        logger.info('Testing get_orders function')
        orders = get_orders()
        self.assertEqual(len(orders), 6)
        self.assertTrue(all(isinstance(order, Order) for order in orders))

    def test_get_orders_filtered(self):
        """
        This function tests the get_orders_filtered function
        """
        logger.info('Testing get_orders_filtered function')
        orders = get_orders_filtered(None)
        self.assertEqual(len(orders), 6)

        orders = get_orders_filtered(Status.in_progress)

        self.assertEqual(len(orders), 4)
        self.assertTrue(orders[0].id == 1)
        self.assertTrue(orders[1].id == 2)
        self.assertTrue(orders[2].id == 4)
        self.assertTrue(orders[3].id == 5)

        orders = get_orders_filtered('invalid status')
        self.assertEqual(len(orders), 6)

        orders = get_orders_filtered('In progress')
        self.assertEqual(len(orders), 4)

    def test_get_order_by_id(self):
        """
        This function tests the get_order_by_id function
        """
        logger.info('Testing get_order_by_id function')
        order = get_order_by_id(1)
        self.assertEqual(order.id, 1)

    def test_get_orders_by_seller(self):
        """
        This function tests the get_orders_by_seller function
        """
        logger.info('Testing get_orders_by_seller function')
        orders = get_orders_by_seller(1)
        self.assertEqual(len(orders), 3)
        self.assertTrue(all(order.seller_id == 1 for order in orders))

    def test_get_orders_by_seller_filtered(self):
        """
        This function tests the get_orders_by_seller_filtered function
        """
        logger.info('Testing get_orders_by_seller_filtered function')
        orders = get_orders_by_seller_filtered(1, None)
        self.assertEqual(len(orders), 3)
        self.assertTrue(all(order.seller_id == 1 for order in orders))

        orders = get_orders_by_seller_filtered(1, Status.in_progress)

        self.assertEqual(len(orders), 2)
        self.assertTrue(all(order.seller_id == 1 for order in orders))
        self.assertTrue(orders[0].id == 1)
        self.assertTrue(orders[1].id == 2)

        orders = get_orders_by_seller_filtered(1, 'invalid status')
        self.assertEqual(len(orders), 3)

        orders = get_orders_by_seller_filtered(1, 'In progress')
        self.assertEqual(len(orders), 2)

    def test_filter_orders_by_status(self):
        """
        This function tests the filter_orders_by_status function
        """
        logger.info('Testing filter_orders_by_status function')
        orders_query = Order.query

        orders = filter_orders_by_status(orders_query, None).all()
        self.assertEqual(len(orders), 6)

        orders = filter_orders_by_status(orders_query, Status.in_progress).all()
        self.assertEqual(len(orders), 4)
        self.assertTrue(all(order.status == Status.in_progress for order in orders))

        orders = filter_orders_by_status(orders_query, status='invalid status').all()
        self.assertEqual(len(orders), 0)

    def test_create_order(self):
        """
        This function tests the create_order function
        """
        logger.info('Testing create_order function')
        order = create_order(1, 'Customer details', Status.in_progress, 1, 1)
        self.assertEqual(order.id, 7)
        self.assertEqual(order.customer_details, 'Customer details')
        self.assertEqual(order.status, Status.in_progress)
        self.assertEqual(order.seller_id, 1)
        self.assertEqual(order.product_id, 1)

    def test_update_order(self):
        """
        This function tests the update_order function
        """
        logger.info('Testing update_order function')
        updated_quantity = 2
        updated_customer_details = 'Updated customer details'
        updated_status = Status.complete
        updated_seller_id = 2
        updated_product_id = 2

        order = get_order_by_id(1)
        updated_order = update_order(1)

        self.assertEqual(order, updated_order)

        updated_order = update_order(1, updated_quantity, updated_customer_details, updated_status, updated_seller_id,
                                     updated_product_id)

        self.assertEqual(updated_order.quantity, updated_quantity)
        self.assertEqual(updated_order.customer_details, updated_customer_details)
        self.assertEqual(updated_order.status, updated_status)
        self.assertEqual(updated_order.seller_id, updated_seller_id)
        self.assertEqual(updated_order.product_id, updated_product_id)

        updated_order = update_order(1, status='invalid status')
        self.assertEqual(updated_order.status, updated_status)

        updated_order = update_order(1, status='In progress')
        self.assertEqual(updated_order.status, Status.in_progress)

        self.assertFalse(update_order(-1))

    def test_delete_order(self):
        """
        This function tests the delete_order function
        """
        logger.info('Testing delete_order function')
        order = get_order_by_id(1)
        orders = get_orders()
        self.assertEqual(len(orders), 6)

        result = delete_order(order.id)

        self.assertTrue(result)
        self.assertFalse(delete_order(order.id))

        orders = get_orders()
        self.assertEqual(len(orders), 5)
        self.assertTrue(order not in orders)

    def test_get_available_statuses(self):
        """
        This function tests the get_available_statuses function
        """
        logger.info('Testing get_available_statuses function')
        statuses = get_available_statuses()
        self.assertEqual(len(statuses), 2)
        self.assertTrue(all(status.label in statuses for status in Status))