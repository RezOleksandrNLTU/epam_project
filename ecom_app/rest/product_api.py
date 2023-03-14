"""
This module contains the ProductAPI class which is used to handle the REST API requests for single product
"""

from flask import request, abort
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators

from ecom_app.service import product_service


# This is the structure of the JSON response
product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'inventory': fields.Integer,
    'ordered': fields.Integer,
}


class ProductAPI(Resource):
    """
    This class is used to handle the REST API requests for products
    """
    @marshal_with(product_fields)
    @login_required
    def get(self, product_id):
        """
        This method is used to handle the GET request for products
        :param product_id: The id of the product to get
        """
        product = product_service.get_product_by_id(product_id)
        if not product:
            abort(404, 'Product not found')
        if not current_user.is_admin and product.seller_id != current_user.id:
            abort(403, 'You are not authorized')
        return product

    @login_required
    def put(self, product_id):
        """
        This method is used to handle the PUT request for products
        :param product_id: The id of the product to update
        """
        product = product_service.get_product_by_id(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        if not current_user.is_admin and product.seller_id != current_user.id:
            return {'message': 'You are not authorized'}, 403

        name, description, price, inventory = None, None, None, None

        if 'name' in request.json:
            name = request.json['name']
            if not validators.length(name, min=1, max=30):
                return {'message': 'Name is not valid'}, 400
        if 'description' in request.json:
            description = request.json['description']
            if not validators.length(description, min=1, max=300):
                return {'message': 'Description is not valid'}, 400
        if 'price' in request.json:
            try:
                price = int(request.json['price'])
            except ValueError:
                return {'message': 'Price is not valid'}, 400

            if not validators.between(price, min=0.01):
                return {'message': 'Price is not valid'}, 400
        if 'inventory' in request.json:
            try:
                inventory = int(request.json['inventory'])
            except ValueError:
                return {'message': 'Inventory is not valid'}, 400

            if not validators.between(inventory, min=0):
                return {'message': 'Inventory is not valid'}, 400

        try:
            product_service.update_product(product_id, name, description, price, inventory)
        except Exception:
            return {'message': 'Error updating product'}, 500

        return {'message': 'Success'}, 200

    @login_required
    def delete(self, product_id):
        """
        This method is used to handle the DELETE request for products
        :param product_id: The id of the product to delete
        """
        product = product_service.get_product_by_id(product_id)
        if not product:
            return {'message': 'Product not found'}, 404
        if not current_user.is_admin and product.seller_id != current_user.id:
            return {'message': 'You are not authorized'}, 403

        try:
            product_service.delete_product(product_id)
        except Exception:
            return {'message': 'Error deleting product'}, 500

        return {'message': 'Success'}, 200