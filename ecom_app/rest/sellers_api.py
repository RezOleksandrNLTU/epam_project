"""
This module contains the REST API for sellers which is used to handle the REST API requests for sellers
"""

import re

from flask import request, abort
from flask_restful import Resource, fields, marshal_with
from flask_login import login_required, current_user
import validators
import phonenumbers
from werkzeug.security import generate_password_hash

from ecom_app.service import seller_service


# This is the structure of the JSON response
sellers_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
}


class SellersAPI(Resource):
    """
    This class is used to handle the REST API requests for sellers
    """
    @marshal_with(sellers_fields)
    @login_required
    def get(self):
        """
        This method is used to handle the GET request for sellers
        """
        if not current_user.is_admin:
            abort(403, 'You are not authorized')
        return seller_service.get_sellers()

    @login_required
    def post(self):
        """
        This method is used to handle the POST request for sellers
        """
        if not current_user.is_admin:
            return {'message': 'You are not authorized'}, 403

        try:
            name = request.json['name']
            email = request.json['email']
            phone = request.json['phone']
            password = request.json['password']
        except KeyError:
            return {'message': 'Invalid input'}, 400

        if not all([validators.length(name, min=1, max=30), validators.email(email),
                    validators.length(password, min=8, max=30)]):
            return {'message': 'Invalid input'}, 400

        try:
            phonenumbers.parse(phone)
        except phonenumbers.phonenumberutil.NumberParseException:
            return {'message': 'Invalid input'}, 400

        if not re.match('[A-Za-z0-9_]+$', password) or not phonenumbers.is_valid_number(phonenumbers.parse(phone)):
            return {'message': 'Invalid input'}, 400

        password = generate_password_hash(password, method='sha256')

        try:
            seller_service.create_seller(name, email, phone, password, is_admin=False)
        except Exception:
            return {'message': 'Error creating seller'}, 500

        return {'message': 'Success'}, 200

