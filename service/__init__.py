"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys

from flask import Flask
from service import config
from .utils import log_handlers
from flask.logging import create_logger

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Dependencies require we import the routes AFTER the Flask app is created
from service import (  # noqa: F401, E402 # pylint: disable=wrong-import-position, wrong-import-order
    models,
    routes,
)

# fmt: off
from .utils import \
    error_handlers  # noqa: F401, E402 # pylint: disable=wrong-import-position

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

create_logger(app).info(70 * "*")
create_logger(app).info("  S E R V I C E   R U N N I N G  ".center(70, "*"))
create_logger(app).info(70 * "*")

try:
    routes.init_db()  # make our SQLAlchemy tables
except Exception as error:
    create_logger(app).critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

create_logger(app).info("Service initialized!")
