from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from .config import config
from flask_jwt_extended import JWTManager
from app.error_handler.jwt_error_handler import setup_jwt_error_handlers
from flask_cors import CORS
import os

# Initialize Flask extensions
db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
jwt_manager = JWTManager()


def create_app(config_name):
    """
    Factory function to create and configure the Flask application.

    This function initializes the Flask app with the given configuration
    settings, sets up the necessary Flask extensions, registers blueprints,
    and applies custom error handlers.

    Parameters:
    -----------
    config_name : str
        The name of the configuration to use (e.g., 'development', 'testing',
        'production').

    Returns:
    --------
    app : Flask
        The configured Flask application instance.
    """
    app = Flask(__name__)

    # Set the secret keys from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Load the configuration object
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initialize Flask extensions with the app instance
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = 'auth.login'

    jwt_manager.init_app(app)

    # Enable Cross-Origin Resource Sharing (CORS) for the API
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

    # Uncomment if custom JWT middleware setup is required
    # setup_jwt_middleware(app)

    # Define the user loader callback for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load the user by ID for Flask-Login.

        This function queries the User model to retrieve the user
        with the specified user ID.

        Parameters:
        -----------
        user_id : int
            The ID of the user to load.

        Returns:
        --------
        user : User
            The User object corresponding to the given user ID,
            or None if no user is found.
        """
        return User.query.get(int(user_id))

    # Register blueprints for different parts of the API
    from .api.v1 import (public, auth, content,
                         assessment, errors,
                         users as users_api,
                         teacher, admin, student)

    app.register_blueprint(public.bp, url_prefix='/api/v1/public')
    app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(content.bp, url_prefix='/api/v1/content')
    app.register_blueprint(assessment.bp, url_prefix='/api/v1/content')
    app.register_blueprint(errors.bp)
    app.register_blueprint(users_api.bp, url_prefix='/api/v1')
    app.register_blueprint(admin.bp, url_prefix='/api/v1/portal')
    app.register_blueprint(teacher.bp, url_prefix='/api/v1/portal')
    app.register_blueprint(student.bp, url_prefix='/api/v1/portal')

    # Setup custom JWT error handlers
    setup_jwt_error_handlers(jwt_manager)

    return app
