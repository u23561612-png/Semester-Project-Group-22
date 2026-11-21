"""
Pick n Pay Wolmaransstad - Application Configuration

Development, testing and production environment settings.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    DEBUG = False
    TESTING = False

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME", "pnp_receiving")


class DevelopmentConfig(Config):

    DEBUG = True


class TestingConfig(Config):

    TESTING = True
    DEBUG = False

    DB_NAME = os.getenv(
        "DB_TEST_NAME",
        "pnp_receiving_test"
    )


class ProductionConfig(Config):

    DEBUG = False
    TESTING = False


configurations = {

    "development": DevelopmentConfig,

    "testing": TestingConfig,

    "production": ProductionConfig

}