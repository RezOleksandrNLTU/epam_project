"""
This module contains functions to work with orders table
"""

from ecom_app.database import db
from ecom_app.models import Order, Status


def get_orders():
    """
    This function returns all orders
    """
    return Order.query.all()


def get_orders_filtered(status):
    """
    This function returns all orders filtered by status
    :param status: status of the order
    """
    if isinstance(status, Status):
        status = status.name

    if isinstance(status, str):
        member_names = Status._member_names_
        if status not in member_names:
            for name in member_names:
                if status == getattr(Status, name).label:
                    status = name
                    break
            else:
                status = None

    order_query = filter_orders_by_status(Order.query, status)

    return order_query.all()


def get_order_by_id(order_id):
    """
    This function returns order by id
    :param order_id: id of the order
    """
    return Order.query.filter_by(id=order_id).first()


def get_orders_by_seller(seller_id):
    """
    This function returns all orders filtered by seller
    :param seller_id: id of the seller
    """
    return Order.query.filter_by(seller_id=seller_id).all()


def get_orders_by_seller_filtered(seller_id, status):
    """
    This function returns all orders filtered by seller and status
    :param seller_id: id of the seller
    :param status: status of the order
    """
    order_query = Order.query.filter_by(seller_id=seller_id)

    if isinstance(status, Status):
        status = status.name

    if isinstance(status, str):
        member_names = Status._member_names_
        if status not in member_names:
            for name in member_names:
                if status == getattr(Status, name).label:
                    status = name
                    break
            else:
                status = None

    if status:
        order_query = filter_orders_by_status(order_query, status)

    return order_query.all()


def filter_orders_by_status(order_query, status):
    """
    This function filters orders by status
    :param order_query: query to filter
    :param status: status of the order
    """
    if status:
        return order_query.filter(Order.status == status)
    else:
        return order_query


def create_order(quantity, customer_details, status, seller_id, product_id):
    """
    This function creates new order
    :param quantity: quantity of the product
    :param customer_details: customer details
    :param status: status of the order
    :param seller_id: id of the seller
    :param product_id: id of the product
    """
    if isinstance(status, Status):
        status = status.name

    if isinstance(status, str):
        member_names = Status._member_names_
        if status not in member_names:
            for name in member_names:
                if status == getattr(Status, name).label:
                    status = name
                    break
    order = Order(quantity=quantity, customer_details=customer_details, status=status, seller_id=seller_id,
                  product_id=product_id)
    db.session.add(order)
    db.session.commit()
    return order


def update_order(order_id, quantity=None, customer_details=None, status=None, seller_id=None, product_id=None):
    """
    This function updates order
    :param order_id: id of the order
    :param quantity: quantity of the product
    :param customer_details: customer details
    :param status: status of the order
    :param seller_id: id of the seller
    :param product_id: id of the product
    """
    order = Order.query.filter_by(id=order_id).first()

    if not order:
        return False
    if quantity:
        order.quantity = quantity
    if customer_details:
        order.customer_details = customer_details

    if isinstance(status, Status):
        status = status.name

    if isinstance(status, str):
        member_names = Status._member_names_
        if status not in member_names:
            for name in member_names:
                if status == getattr(Status, name).label:
                    status = name
                    break
            else:
                status = None

    if status:
        order.status = status
    if seller_id:
        order.seller_id = seller_id
    if product_id:
        order.product_id = product_id

    db.session.commit()
    return order


def delete_order(order_id):
    """
    This function deletes order
    :param order_id: id of the order
    """
    order = Order.query.filter_by(id=order_id).first()

    if not order:
        return False

    db.session.delete(order)
    db.session.commit()
    return True


def get_available_statuses():
    """
    This function returns all available statuses
    """
    return [status.label for status in Status]
