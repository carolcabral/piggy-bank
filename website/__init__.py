from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# Create database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    '''Creates Flask application'''
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ahsae'  # Get from env variable
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    # Initialize database
    db.init_app(app)

    # Register Blueprints
    from .views import views

    app.register_blueprint(views, url_prefix="/")

    # Create database if it does not exist
    #from .models import User, Entry
    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        # TODO: Database básica para categorias
        print('Created Database!')
