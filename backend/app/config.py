#!/usr/bin/env python3

import os
from datetime import timedelta
from dotenv import load_dotenv

class Config:
    """
    Base configuration class for the application.

    This class contains the default configuration settings that are shared
    across all environments (development, testing, production). It includes
    settings for database connections, email server, JWT, and other necessary
    configurations.

    Attributes:
    -----------
    DB_USERNAME : str
        The username for the database connection (default: 'root').
    DB_PASSWORD : str
        The password for the database connection (default: 'root').
    DB_HOST : str
        The host address of the database server (default: 'localhost').
    DB_PORT : str
        The port number for the database connection (default: '3306').
    DEV_DB_NAME : str
        The name of the development database (default: 'QADB').
    TEST_DB_NAME : str
        The name of the testing database (default: 'Test_QADB').
    PROD_DB_NAME : str
        The name of the production database (default: 'Prod_QADB').
    SQLALCHEMY_TRACK_MODIFICATIONS : bool
        Tracks modifications of objects and emits signals (default: False).
    SECRET_KEY : str
        The secret key for securing sessions and cookies.
    MAIL_SERVER : str
        The mail server address for sending emails (default: 'smtp.googlemail.com').
    MAIL_PORT : int
        The port number for the mail server (default: 587).
    MAIL_USE_TLS : bool
        Whether to use TLS for secure email sending (default: True).
    MAIL_USERNAME : str
        The username for the mail server.
    MAIL_PASSWORD : str
        The password for the mail server.
    MAIL_SUBJECT_PREFIX : str
        The subject prefix for outgoing emails (default: '[Qur`an Academy]').
    MAIL_SENDER : str
        The sender's email address for outgoing emails.
    JWT_SECRET_KEY : str
        The secret key used for encoding JWT tokens.
    JWT_ACCESS_TOKEN_EXPIRES : timedelta
        The expiration time for JWT access tokens (default: 1 day).
    """

    load_dotenv()
    DB_USERNAME = os.getenv('DB_USERNAME', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'root')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DEV_DB_NAME = os.getenv('DEV_DB_NAME', 'QADB')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'Test_QADB')
    PROD_DB_NAME = os.getenv('PROD_DB_NAME', 'Prod_QADB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = '[Qur`an Academy]'
    MAIL_SENDER = os.environ.get('MAIL_SENDER', 'Qur\'an Academy Admin <youssefessam5623@gmail.com>')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    @staticmethod  # type: ignore
    def init_app(app):
        """
        Initialize the application with the provided configuration.

        This method is a placeholder for any initialization steps required
        for the app when a specific configuration is applied.

        Parameters:
        -----------
        app : Flask app instance
            The Flask application instance to be initialized.
        """
        pass


class DevelopmentConfig(Config):
    """
    Development configuration class.

    This class inherits from the base Config class and overrides specific
    settings for development purposes, such as enabling debug mode and
    setting a shorter JWT expiration time.

    Attributes:
    -----------
    DEBUG : bool
        Enables or disables debug mode (default: True).
    SQLALCHEMY_DATABASE_URI : str
        The database URI for the development environment.
    JWT_ACCESS_TOKEN_EXPIRES : timedelta
        The expiration time for JWT access tokens in development (default: 12 hours).
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DEV_DB_NAME}'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)


class TestConfig(Config):
    """
    Testing configuration class.

    This class inherits from the base Config class and overrides specific
    settings for testing purposes, such as enabling testing mode and
    setting the database URI for testing.

    Attributes:
    -----------
    TESTING : bool
        Enables or disables testing mode (default: True).
    SQLALCHEMY_DATABASE_URI : str
        The database URI for the testing environment.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.TEST_DB_NAME}'


class ProductionConfig(Config):
    """
    Production configuration class.

    This class inherits from the base Config class and overrides specific
    settings for production purposes, such as setting the database URI for
    the production environment and a longer JWT expiration time.

    Attributes:
    -----------
    SQLALCHEMY_DATABASE_URI : str
        The database URI for the production environment.
    JWT_ACCESS_TOKEN_EXPIRES : timedelta
        The expiration time for JWT access tokens in production (default: 7 days).
    """
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.PROD_DB_NAME}'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
