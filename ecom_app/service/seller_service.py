"""
This module contains functions to work with sellers table
"""

from ecom_app.database import db
from ecom_app.models import Seller


def get_sellers():
    """
    This function returns all sellers
    """
    return Seller.query.all()


def get_seller_by_id(seller_id):
    """
    This function returns seller by id
    :param seller_id: id of the seller
    """
    return Seller.query.filter_by(id=seller_id).first()


def get_seller_by_email(email):
    """
    This function returns seller by email
    :param email: email of the seller
    """
    return Seller.query.filter_by(email=email).first()


def create_seller(name, email, phone, password, is_admin):
    """
    This function creates new seller
    :param name: name of the seller
    :param email: email of the seller
    :param phone: phone of the seller
    :param password: password of the seller
    :param is_admin: is seller admin
    """

    seller = Seller(name=name, email=email, phone=phone, password=password, is_admin=is_admin)
    db.session.add(seller)
    db.session.commit()
    return seller


def update_seller(seller_id, name=None, email=None, phone=None, password=None, is_admin=None):
    """
    This function updates seller
    :param seller_id: id of the seller
    :param name: name of the seller
    :param email: email of the seller
    :param phone: phone of the seller
    :param password: password of the seller
    :param is_admin: is seller admin
    """
    seller = Seller.query.filter_by(id=seller_id).first()

    if not seller:
        return False

    if name:
        seller.name = name
    if email:
        seller.email = email
    if phone:
        seller.phone = phone
    if password:
        seller.password = password
    if is_admin:
        seller.is_admin = is_admin

    db.session.commit()
    return seller


def delete_seller(seller_id):
    """
    This function deletes seller
    :param seller_id: id of the seller
    """
    seller = Seller.query.filter_by(id=seller_id).first()

    if not seller:
        return False

    db.session.delete(seller)
    db.session.commit()
    return True
