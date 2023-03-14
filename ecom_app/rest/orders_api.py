"""
This module contains the OrderAPI class which is used to handle the REST API requests for single order
"""

from flask import request, abort
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators

from ecom_app.service import order_service, product_service


# This is the structure of the JSON response
orders_fields = {
    'id': fields.Integer,
    'product_id': fields.Integer,
    'product_name': fields.String(attribute=lambda x: x.product.name),
    'quantity': fields.Integer,
    'total': fields.Float(attribute=lambda x: x.total_cost),
    'date': fields.DateTime(dt_format='iso8601'),
    'customer_details': fields.String,
    'status': fields.String(attribute=lambda x: x.status.label),
}


class OrdersAPI(Resource):
    """
    This class is used to handle the REST API requests for orders
    """
    @marshal_with(orders_fields)
    @login_required
    def get(self):
        """
        This method is used to handle the GET request for orders
        """
        status = request.args.get('status')

        if status:
            if status not in order_service.get_available_statuses():
                abort(400, "Status is not valid")
            if current_user.is_admin:
                orders = order_service.get_orders_filtered(status)
            else:
                orders = order_service.get_orders_by_seller_filtered(current_user.id, status)
        else:
            if current_user.is_admin:
                orders = order_service.get_orders()
            else:
                orders = order_service.get_orders_by_seller(current_user.id)

        return orders

    @login_required
    def post(self):
        """
        This method is used to handle the POST request for orders
        """
        try:
            product_id = request.json['product_id']
            quantity = request.json['quantity']
            customer_details = request.json['customer_details']
            status = request.json['status']
        except KeyError:
            return {'message': 'Invalid input'}, 400

        try:
            product_id = int(product_id)
            quantity = int(quantity)
        except ValueError:
            return {'message': 'Invalid input'}, 400

        if not all([validators.between(quantity, min=1), validators.length(customer_details, min=1, max=300)]):
            return {'message': 'Invalid input'}, 400

        if not product_service.get_product_by_id(product_id):
            return {'message': 'Product is not valid'}, 400

        if status not in order_service.get_available_statuses():
            return {'message': 'Status is not valid'}, 400

        order = order_service.create_order(quantity, customer_details, status, current_user.id, product_id)

        return {'message': 'Order created', 'order_id': order.id}, 201
