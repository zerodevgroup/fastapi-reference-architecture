# /app/config.py

import os

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DAO_URI = os.getenv("DAO_URI")

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    DAO_URI = os.getenv("DAO_URI")

app_config = {
    "development": Development,
    "production": Production,
}
