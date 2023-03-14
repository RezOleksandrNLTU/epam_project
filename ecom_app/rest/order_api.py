"""
This module contains the OrderAPI class which is used to handle the REST API requests for single order
"""

from flask import request, abort
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators

from ecom_app.service import order_service, product_service


# This is the structure of the JSON response
order_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'product_name': fields.String(attribute=lambda x: x.product.name),
    'quantity': fields.Integer,
    'total': fields.Float(attribute=lambda x: x.total_cost),
    'date': fields.DateTime(dt_format='iso8601'),
    'customer_details': fields.String,
    'status': fields.String(attribute=lambda x: x.status.label),
}


class OrderAPI(Resource):
    """
    This class is used to handle the REST API requests for orders
    """
    @marshal_with(order_fields)
    @login_required
    def get(self, order_id):
        """
        This method is used to handle the GET request for orders
        :param order_id: The id of the order to get
        """
        order = order_service.get_order_by_id(order_id)
        if not order:
            abort(404, "Order not found")
        if not current_user.is_admin and order.seller_id != current_user.id:
            abort(403, "You are not authorized")
        return order

    @login_required
    def put(self, order_id):
        """
        This method is used to handle the PUT request for orders
        :param order_id: The id of the order to update
        """
        order = order_service.get_order_by_id(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        if not current_user.is_admin and order.seller_id != current_user.id:
            return {'message': 'You are not authorized'}, 403

        product, quantity, customer_details, status = None, None, None, None

        if 'product' in request.json:
            product = request.json['product']
            if not product_service.get_product_by_id(product):
                return {'message': 'Product is not valid'}, 400

        if 'quantity' in request.json:
            try:
                quantity = int(request.json['quantity'])
            except ValueError:
                return {'message': 'Quantity is not valid'}, 400
            if not validators.between(quantity, min=1):
                return {'message': 'Quantity is not valid'}, 400

        if 'customer_details' in request.json:
            customer_details = request.json['customer_details']
            if not validators.length(customer_details, min=1, max=300):
                return {'message': 'Customer details is not valid'}, 400

        if 'status' in request.json:
            status = request.json['status']
            if status not in order_service.get_available_statuses():
                return {'message': 'Status is not valid'}, 400

        try:
            order_service.update_order(order_id, quantity, customer_details, status, None, product)
        except Exception:
            return {'message': 'Error updating order'}, 500

        return {'message': 'Success'}, 200

    @login_required
    def delete(self, order_id):
        """
        This method is used to handle the DELETE request for orders
        :param order_id: The id of the order to delete
        """
        order = order_service.get_order_by_id(order_id)
        if not order:
            return {'message': 'Order not found'}, 404
        if not current_user.is_admin and order.seller_id != current_user.id:
            return {'message': 'You are not authorized'}, 403

        try:
            order_service.delete_order(order_id)
        except Exception:
            return {'message': 'Error deleting order'}, 500

        return {'message': 'Success'}, 200