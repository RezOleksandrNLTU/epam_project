"""
This module contains the SellerAPI class which is used to handle the REST API requests for single seller
"""

import re

from flask import request
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators
import phonenumbers
from werkzeug.security import generate_password_hash

from ecom_app.service import seller_service


# This is the structure of the JSON response
seller_fields = {
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
}


class SellerAPI(Resource):
    """
    This class is used to handle the REST API requests for sellers
    """
    @marshal_with(seller_fields)
    @login_required
    def get(self, seller_id=None):
        """
        This method is used to handle the GET request for sellers
        :param seller_id: The id of the seller
        """
        if seller_id and seller_id != current_user.id and not current_user.is_admin:
            return {'message': 'You are not authorized'}, 403
        if not seller_id:
            seller_id = current_user.id
        seller = seller_service.get_seller_by_id(seller_id)
        if not seller:
            return {'message': 'Seller not found'}, 404
        return seller

    @login_required
    def put(self, seller_id=None):
        """
        This method is used to handle the PUT request for sellers
        :param seller_id: The id of the seller to update
        """
        if seller_id and seller_id != current_user.id and not current_user.is_admin:
            return {'message': 'You are not authorized'}, 403
        if not seller_id:
            seller_id = current_user.id
        seller = seller_service.get_seller_by_id(seller_id)
        if not seller:
            return {'message': 'Seller not found'}, 404

        name, email, phone, password = None, None, None, None

        if 'name' in request.json:
            name = request.json['name']
            if not validators.length(name, min=1, max=30):
                return {'message': 'Name is not valid'}, 400
        if 'email' in request.json:
            email = request.json['email']
            if not validators.email(email):
                return {'message': 'Email is not valid'}, 400
        if 'phone' in request.json:
            phone = request.json['phone']
            try:
                a = phonenumbers.parse(phone)
                if not phonenumbers.is_valid_number(phonenumbers.parse(phone)):
                    return {'message': 'Phone is not valid'}, 400
            except phonenumbers.phonenumberutil.NumberParseException:
                return {'message': 'Phone is not valid'}, 400

        if 'password' in request.json and current_user.is_admin:
            password = request.json['password']
            if not validators.length(password, min=8, max=30):
                return {'message': 'Password is not valid'}, 400

            if not re.match('[A-Za-z0-9_]+$', password):
                return {'message': 'Password is not valid'}, 400

            password = generate_password_hash(password, method='sha256')

        try:
            update_successful = seller_service.update_seller(seller_id, name, email, phone, password)
        except Exception:
            return {'message': 'Error updating seller'}, 500

        if not update_successful:
            return {'message': 'Seller not found'}, 404

        return {'message': 'Success'}, 200

    @login_required
    def delete(self, seller_id=None):
        """
        This method is used to handle the DELETE request for sellers
        :param seller_id: The id of the seller to delete
        """
        if not current_user.is_admin:
            return {'message': 'You are not authorized'}, 403

        if not seller_id:
            return {'message': 'Seller not found'}, 404

        try:
            delete_successful = seller_service.delete_seller(seller_id)
        except Exception:
            return {'message': 'Error deleting seller'}, 500

        if not delete_successful:
            return {'message': 'Seller not found'}, 404

        return {'message': 'Success'}, 200
