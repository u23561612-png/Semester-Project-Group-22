"""
Pick n Pay Wolmaransstad - Database Connection
"""

import mysql.connector

from flask import current_app, has_app_context
from config import Config


def get_db_connection():

    settings = (
        current_app.config
        if has_app_context()
        else vars(Config)
    )

    connection = mysql.connector.connect(

        host=settings["DB_HOST"],

        port=settings["DB_PORT"],

        user=settings["DB_USER"],

        password=settings["DB_PASSWORD"],

        database=settings["DB_NAME"]

    )

    return connection