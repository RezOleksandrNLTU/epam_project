"""
This module contains the views for the auth blueprint
"""

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from ecom_app.service import seller_service


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """
    This method is used to handle the GET request for the login page
    """
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """
    This method is used to handle the POST request for the login page
    """
    email = request.form.get('email')
    password = request.form.get('password')

    seller = seller_service.get_seller_by_email(email)
    if not seller or not check_password_hash(seller.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(seller, remember=True)
    return redirect(url_for('sellers.profile'))


@auth.route('/logout')
@login_required
def logout():
    """
    This method is used to handle the GET request for the logout page
    """
    logout_user()
    return redirect(url_for('auth.login'))
