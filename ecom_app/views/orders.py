"""
This module contains the views for the orders blueprint
"""

from flask import Blueprint, render_template
from flask_login import login_required


orders = Blueprint('orders', __name__)


@orders.route('/orders')
@login_required
def orders_():
    """
    This method is used to handle the GET request for the orders page
    """
    return render_template('orders.html')


@orders.route('/orders/edit', defaults={'order_id': None})
@orders.route('/orders/edit/<int:order_id>')
@login_required
def edit_order(order_id):
    """
    This method is used to handle the GET request for the edit order page
    :param order_id: The id of the order to edit
    """
    return render_template('edit_order.html')


@orders.route('/orders/add')
@login_required
def add_order():
    """
    This method is used to handle the GET request for the add order page
    """
    return render_template('add_order.html')
