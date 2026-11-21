"""
Pick n Pay Wolmaransstad - Receiving Stock System

Main Flask application.
Group 22
"""

import os
import logging

from flask import Flask, render_template

from config import configurations
from routes.api import api


# Create Flask application

app = Flask(__name__)


# Load application configuration

environment = os.getenv(
    "APP_ENV",
    "development"
)

if environment not in configurations:

    raise ValueError("Invalid application environment.")

app.config.from_object(
    configurations[environment]
)


# Configure application logging

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)


# Register API Blueprint

app.register_blueprint(api)


# Home page

@app.route("/")
def home():

    return render_template("index.html")


# Run Flask application

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001
    )