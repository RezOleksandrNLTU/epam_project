"""
The flask application package. Contains the application factory
"""

import os

import click
from flask import Flask
from flask_login import LoginManager
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

from ecom_app import database, views, rest
from ecom_app.models import Seller, Product, Order


def create_app(test_config=None):
    """
    This function creates the flask application
    """
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.urandom(24),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
        )
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.db.init_app(app)
    database.migrate.init_app(app, database.db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Seller.query.get(int(user_id))

    @app.cli.command('create_admin')
    @click.argument('name')
    @click.argument('email')
    @click.argument('phone')
    @click.argument('password')
    @with_appcontext
    def create_admin(name, email, phone, password):
        """
        This function creates an admin user
        """
        password = generate_password_hash(password, method='sha256')
        seller = Seller(name=name, email=email, phone=phone, password=password, is_admin=True)
        database.db.session.add(seller)
        database.db.session.commit()
        click.echo('Admin created successfully')

    app.register_blueprint(views.auth)
    app.register_blueprint(views.sellers)
    app.register_blueprint(views.products)
    app.register_blueprint(views.orders)

    app.register_blueprint(rest.rest_api, url_prefix='/api')

    return app
