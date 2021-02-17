from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

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
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Create database if it does not exist
    from .models import User, Entry
    create_database(app)

    # Loads user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        ## TODO: Database básica para categorias
        print('Created Database!')
