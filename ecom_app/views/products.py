"""
This module contains the views for the products blueprint
"""

from flask import Blueprint, render_template
from flask_login import login_required


products = Blueprint('products', __name__)


@products.route('/products')
@login_required
def products_():
    """
    This method is used to handle the GET request for the products page
    """
    return render_template('products.html')


@products.route('/products/edit', defaults={'product_id': None})
@products.route('/products/edit/<int:product_id>')
@login_required
def edit_product(product_id):
    """
    This method is used to handle the GET request for the edit product page
    :param product_id: The id of the product to edit
    """
    return render_template('edit_product.html')


@products.route('/products/add')
@login_required
def add_product():
    """
    This method is used to handle the GET request for the add product page
    """
    return render_template('add_product.html')

