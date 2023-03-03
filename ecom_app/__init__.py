import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://ecom:ecom@localhost:3306/ecom",
    )
    db = SQLAlchemy()
    db.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app
