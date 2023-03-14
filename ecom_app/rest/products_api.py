"""
This module contains the ProductsAPI class which is used to handle the REST API requests for products
"""

from flask import request, abort
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators

from ecom_app.service import product_service


# This is the structure of the JSON response
products_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'inventory': fields.Integer,
    'ordered': fields.Integer,
}


class ProductsAPI(Resource):
    """
    This class is used to handle the REST API requests for products
    """
    @marshal_with(products_fields)
    @login_required
    def get(self):
        """
        This method is used to handle the GET request for products
        """
        inventory_from = request.args.get('inventory_from')
        inventory_to = request.args.get('inventory_to')
        ordered_from = request.args.get('ordered_from')
        ordered_to = request.args.get('ordered_to')

        if inventory_from:
            try:
                inventory_from = int(inventory_from)
            except ValueError:
                abort(400, 'Invalid input')

            if not validators.between(inventory_from, min=0):
                abort(400, 'Invalid input')

        if inventory_to:
            try:
                inventory_to = int(inventory_to)
            except ValueError:
                abort(400, 'Invalid input')

            if not validators.between(inventory_to, min=0):
                abort(400, 'Invalid input')

        if ordered_from:
            try:
                ordered_from = int(ordered_from)
            except ValueError:
                abort(400, 'Invalid input')

            if not validators.between(ordered_from, min=0):
                abort(400, 'Invalid input')

        if ordered_to:
            try:
                ordered_to = int(ordered_to)
            except ValueError:
                abort(400, 'Invalid input')

            if not validators.between(ordered_to, min=0):
                abort(400, 'Invalid input')

        if current_user.is_admin:
            if any([inventory_from, inventory_to, ordered_from, ordered_to]):
                products = product_service.get_products_filtered(inventory_from, inventory_to, ordered_from, ordered_to)
            else:
                products = product_service.get_products()
        else:
            if any([inventory_from, inventory_to, ordered_from, ordered_to]):
                products = product_service.get_products_by_seller_filtered(current_user.id, inventory_from,
                                                                           inventory_to, ordered_from, ordered_to)
            else:
                products = product_service.get_products_by_seller(current_user.id)

        return products

    @login_required
    def post(self):
        """
        This method is used to handle the POST request for products
        """

        try:
            name = request.json['name']
            description = request.json['description']
        except KeyError:
            return {'message': 'Invalid input'}, 400

        try:
            price = int(request.json['price'])
            inventory = int(request.json['inventory'])
        except ValueError:
            return {'message': 'Invalid input'}, 400

        if not all([validators.length(name, min=1, max=30), validators.length(description, min=1, max=300),
                   validators.between(price, min=0.01), validators.between(price, min=0)]):
            return {'message': 'Invalid input'}, 400

        try:
            product_service.create_product(name, description, price, inventory, current_user.id)
        except Exception:
            return {'message': 'Error creating product'}, 500

        return {'message': 'Success'}, 200
