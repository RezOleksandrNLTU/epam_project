"""
This file contains the models for the database.
"""

import enum

from sqlalchemy.sql import func as sql_func
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, Boolean, Enum, select, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import force_auto_coercion
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import *
from ecom_app.database import db

force_auto_coercion()


class Status(enum.Enum):
    """
    This class is used to represent the status of the order as an enum
    """
    complete = 1
    in_progress = 2


Status.complete.label = 'Complete'
Status.in_progress.label = 'In progress'


class Order(db.Model):
    """
    This class represents the orders table
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, server_default=sql_func.now())
    quantity = Column(Integer, nullable=False)
    customer_details = Column(String(300), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.in_progress)

    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    # product = relationship('Product', backref='product')

    def __repr__(self):
        """
        This function returns the string representation of the order
        """
        return f'{self.id}'

    @hybrid_property
    def total_cost(self):
        """
        This function returns the total cost of the order
        """
        return self.quantity * self.product.price


class Seller(UserMixin, db.Model):
    """
    This class represents the sellers table
    """
    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    products = relationship('Product', backref='seller', cascade="all,delete")
    orders = relationship('Order', backref='seller', cascade="all,delete")

    def __repr__(self):
        """
        This function returns the string representation of the seller
        """
        return f'{self.id} - {self.name}'


class Product(db.Model):
    """
    This class represents the products table
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(300), nullable=False)
    price = Column(Float, nullable=False)
    inventory = Column(Integer, nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)

    orders = relationship('Order', backref='product', cascade="all,delete")

    def __repr__(self):
        """
        This function returns the string representation of the product
        """
        return f'{self.id} - {self.name}'

    @hybrid_property
    def ordered(self):
        """
        This function returns the total quantity of the product that has been ordered
        """
        return sum([order.quantity for order in self.orders if order.status == Status.in_progress])

    @ordered.expression
    def ordered(cls):
        """
        This function returns the total quantity of the product that has been ordered
        """

        return select(func.sum(Order.quantity)).where(
            and_(Order.product_id == cls.id, Order.status == Status.in_progress)
        ).label('ordered')