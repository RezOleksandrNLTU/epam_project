"""
This module contains the views for the sellers blueprint
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user


sellers = Blueprint('sellers', __name__)


@sellers.route('/')
@sellers.route('/profile')
@login_required
def profile():
    """
    This method is used to handle the GET request for the profile page
    """
    return render_template('profile.html')


@sellers.route('/edit_profile')
@login_required
def edit_profile():
    """
    This method is used to handle the GET request for the edit profile page
    """
    return render_template('edit_profile.html')


@sellers.route('/sellers')
@login_required
def sellers_():
    """
    This method is used to handle the GET request for the sellers page
    """
    if current_user.is_admin:
        return render_template('sellers.html')
    return 'You are not authorized to view this page', 403


@sellers.route('/sellers/edit', defaults={'seller_id': None})
@sellers.route('/sellers/edit/<int:seller_id>')
@login_required
def edit_seller(seller_id):
    """
    This method is used to handle the GET request for the edit seller page
    :param seller_id: The id of the seller to edit
    """
    if current_user.is_admin:
        return render_template('edit_seller.html')
    return 'You are not authorized to view this page', 403


@sellers.route('/sellers/add')
@login_required
def add_seller():
    """
    This method is used to handle the GET request for the add seller page
    """
    if current_user.is_admin:
        return render_template('add_seller.html')
    return 'You are not authorized to view this page', 403