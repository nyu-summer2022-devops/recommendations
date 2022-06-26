"""
My Service

Describe what your service does here
"""

import logging
import os
import sys

from flask import Flask, abort, jsonify, make_response, request, url_for
# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy

from service.models import DataValidationError, Recommendation

# Import Flask application
from . import app
from .utils import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )

######################################################################
# ADD A NEW RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=['POST'])
def create_recommendations():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body this is posted
    """
    app.logger.info("Request to create a rec")
    check_content_type("application/json")
    rec = Recommendation()
    app.logger.info(request.get_json())
    rec.deserialize(request.get_json())
    rec.create()
    message = rec.serialize()
    # location_url = url_for("get_recommendations", rec_id = rec.id, _external=True)

    # return jsonify(message), status.HTTP_201_CREATED, {"Location", location_url}
    return jsonify(message), status.HTTP_201_CREATED

######################################################################
# Read A Recommendation
######################################################################
@app.route("/recommendations/<int:id>", methods=["GET"])
def get_recommendations(id):
    """
    Retrieve a single Recommendation

    This endpoint will return a Recommendation based on it's id
    """
    app.logger.info("Request for Recommendation with id: %s", id)
    rec = Recommendation.find(id)
    if not rec:
        abort(status.HTTP_404_NOT_FOUND, f"Recommendation with id '{id}' was not found.")

    app.logger.info("Returning recommendation: %s", rec.product_name)
    return jsonify(rec.serialize()), status.HTTP_200_OK

######################################################################
# List all the Recommendations
######################################################################
@app.route("/recommendations", methods=["GET"])
def list_recommendations():
    """
    Retrieves all recommendations

    This endpoint will return all the recommendations available
    """
    app.logger.info("Request to list all the recommendations")
    rec = Recommendation.all()
    message = [recommendation.serialize() for recommendation in rec]
    return jsonify(message), status.HTTP_200_OK 

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Recommendation.init_db(app)

def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )

