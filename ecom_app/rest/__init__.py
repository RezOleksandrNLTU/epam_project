"""
This module contains the blueprint for the REST API.
"""

from flask import Blueprint
from flask_restful import Api

from .sellers_api import SellersAPI
from .seller_api import SellerAPI
from .products_api import ProductsAPI
from .product_api import ProductAPI
from .orders_api import OrdersAPI
from .order_api import OrderAPI


rest_api = Blueprint('rest_api', __name__)
api = Api(rest_api)

api.add_resource(SellerAPI, '/seller/<int:seller_id>', '/seller')
api.add_resource(SellersAPI, '/sellers')
api.add_resource(ProductAPI, '/product/<int:product_id>', '/product')
api.add_resource(ProductsAPI, '/products')
api.add_resource(OrderAPI, '/order/<int:order_id>', '/order')
api.add_resource(OrdersAPI, '/orders')
