"""
This module contains functions to work with products table
"""

from ecom_app.database import db
from ecom_app.models import Product


def get_products():
    """
    This function returns all products
    """
    return Product.query.all()


def get_products_filtered(inventory_from, inventory_to, ordered_from, ordered_to):
    """
    This function returns all products filtered by inventory and ordered
    :param inventory_from: inventory start range value
    :param inventory_to: inventory end range value
    :param ordered_from: ordered start range value
    :param ordered_to: ordered end range value
    """
    product_query = Product.query

    if inventory_from or inventory_to:
        product_query = filter_products_by_inventory(product_query, inventory_from, inventory_to)

    if ordered_from or ordered_to:
        product_query = filter_products_by_ordered(product_query, ordered_from, ordered_to)

    return product_query.all()


def get_product_by_id(product_id):
    """
    This function returns product by id
    :param product_id: id of the product
    """
    return Product.query.filter_by(id=product_id).first()


def get_product_by_name(name):
    """
    This function returns product by name
    :param name: name of the product
    """
    return Product.query.filter_by(name=name).first()


def get_products_by_seller(seller_id):
    """
    This function returns all products filtered by seller
    :param seller_id: id of the seller
    """
    return Product.query.filter_by(seller_id=seller_id).all()


def get_products_by_seller_filtered(seller_id, inventory_from, inventory_to, ordered_from, ordered_to):
    """
    This function returns all products filtered by seller and inventory and ordered
    :param seller_id: id of the seller
    :param inventory_from: inventory start range value
    :param inventory_to: inventory end range value
    :param ordered_from: ordered start range value
    :param ordered_to: ordered end range value
    """
    product_query = Product.query.filter_by(seller_id=seller_id)

    if inventory_from or inventory_to:
        product_query = filter_products_by_inventory(product_query, inventory_from, inventory_to)

    if ordered_from or ordered_to:
        product_query = filter_products_by_ordered(product_query, ordered_from, ordered_to)

    return product_query.all()


def filter_products_by_inventory(product_query, inventory_from, inventory_to):
    """
    This function filters products by inventory
    :param product_query: query to filter
    :param inventory_from: inventory start range value
    :param inventory_to: inventory end range value
    """
    if inventory_from and inventory_to:
        return product_query.filter(Product.inventory >= inventory_from, Product.inventory <= inventory_to)
    elif inventory_from:
        return product_query.filter(Product.inventory >= inventory_from)
    elif inventory_to:
        return product_query.filter(Product.inventory <= inventory_to)
    else:
        return product_query


def filter_products_by_ordered(product_query, ordered_from, ordered_to):
    """
    This function filters products by ordered
    :param product_query: query to filter
    :param ordered_from: ordered start range value
    :param ordered_to: ordered end range value
    """
    if ordered_from and ordered_to:
        return product_query.filter(Product.ordered >= ordered_from, Product.ordered <= ordered_to)
    elif ordered_from:
        return product_query.filter(Product.ordered >= ordered_from)
    elif ordered_to:
        return product_query.filter(Product.ordered <= ordered_to)
    else:
        return product_query


def create_product(name, description, price, inventory, seller_id):
    """
    This function creates a new product
    :param name: name of the product
    :param description: description of the product
    :param price: price of the product
    :param inventory: inventory of the product
    :param seller_id: id of the seller
    """
    product = Product(name=name, description=description, price=price, inventory=inventory, seller_id=seller_id)
    db.session.add(product)
    db.session.commit()
    return product


def update_product(product_id, name=None, description=None, price=None, inventory=None, seller_id=None):
    """
    This function updates a product
    :param product_id: id of the product
    :param name: name of the product
    :param description: description of the product
    :param price: price of the product
    :param inventory: inventory of the product
    :param seller_id: id of the seller
    """
    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return False

    if name:
        product.name = name
    if description:
        product.description = description
    if price:
        product.price = price
    if inventory:
        product.inventory = inventory
    if seller_id:
        product.seller_id = seller_id

    db.session.commit()
    return product


def delete_product(product_id):
    """
    This function deletes a product
    :param product_id: id of the product
    """
    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return False

    db.session.delete(product)
    db.session.commit()
    return True
