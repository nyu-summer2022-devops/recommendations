"""
My Service

Describe what your service does here
"""
from flask import abort, jsonify, make_response, request, url_for
from flask.logging import create_logger

from service.models import Recommendation

# Import Flask application
from . import app
from .utils import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    create_logger(app).info("Request for Root URL ")
    return app.send_static_file("index.html")


######################################################################
# ADD A NEW RECOMMENDATION
######################################################################
@app.route("/recommendations", methods=["POST"])
def create_recommendations():
    """
    Creates a Recommendation
    This endpoint will create a Recommendation based the data in the body this is posted
    """
    create_logger(app).info("Request to create a rec")
    check_content_type("application/json")
    rec = Recommendation()
    create_logger(app).info(request.get_json())
    rec.deserialize(request.get_json())
    rec.create()
    message = rec.serialize()
    location_url = url_for("get_recommendations", id=rec.id, _external=True)
    resp = make_response(jsonify(message), status.HTTP_201_CREATED)
    resp.headers["Location"] = location_url
    return resp


######################################################################
# Read A Recommendation
######################################################################
@app.route("/recommendations/<int:id>", methods=["GET"])
def get_recommendations(id):
    """
    Retrieve a single Recommendation

    This endpoint will return a Recommendation based on it's id
    """
    create_logger(app).info("Request for Recommendation with id: %s", id)
    rec = Recommendation.find(id)
    if not rec:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{id}' was not found.",
        )

    create_logger(app).info("Returning recommendation: %s", rec.product_name)
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
    create_logger(app).info("Request to list all the recommendations")

    rec = []
    product_id = request.args.get('product_id')
    rec_type = request.args.get('rec_type')
    rec = Recommendation.find_by_params(product_id, rec_type)

    if not rec:
        abort(
            status.HTTP_404_NOT_FOUND,
            "Recommendation was not found.",
        )
    message = [recommendation.serialize() for recommendation in rec]
    return jsonify(message), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>", methods=["PUT"])
def update_recommendations(id):
    """
    Update a Recommendation

    This endpoint will update a Recommendation based the body that is posted
    """
    create_logger(app).info("Request to update Recommendation with id: %s", id)
    check_content_type("application/json")

    rec = Recommendation.find(id)
    if not rec:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{id}' was not found.",
        )

    rec.deserialize(request.get_json())
    rec.id = id
    rec.update()

    create_logger(app).info("Recommendation with ID [%s] updated.", rec.id)
    return jsonify(rec.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>", methods=["DELETE"])
def delete_recommendations(id):
    """
    Delete a Recommendation
    This endpoint will delete a Recommendation based the id specified in the path
    """
    create_logger(app).info("Request to delete recommendation with id: %s", id)
    rec = Recommendation.find(id)
    if rec:
        rec.delete()

    create_logger(app).info("Recommendation with ID [%s] delete complete.", id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# Like A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>/like", methods=["PUT"])
def like_recommendations(id):
    """
    Like a Recommendation

    This endpoint will like a Recommendation based on the id
    """
    create_logger(app).info("Request to like Recommendation with id: %s", id)
    check_content_type("application/json")

    rec = Recommendation.find(id)
    if not rec:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{id}' was not found.",
        )

    rec.deserialize(request.get_json())
    rec.id = id
    rec.like_num += 1
    rec.update()

    create_logger(app).info("Recommendation with ID [%s] is liked.", rec.id)
    return jsonify(rec.serialize()), status.HTTP_200_OK


######################################################################
# Unlike A RECOMMENDATION
######################################################################
@app.route("/recommendations/<int:id>/unlike", methods=["PUT"])
def unlike_recommendations(id):
    """
    Unlike a Recommendation

    This endpoint will unlike a Recommendation based on the id
    """
    create_logger(app).info("Request to unlike Recommendation with id: %s", id)
    check_content_type("application/json")

    rec = Recommendation.find(id)
    if not rec:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Recommendation with id '{id}' was not found.",
        )

    rec.deserialize(request.get_json())
    rec.id = id

    if rec.like_num >= 1:
        rec.like_num -= 1
    rec.update()

    create_logger(app).info("Recommendation with ID [%s] is unliked.", rec.id)
    return jsonify(rec.serialize()), status.HTTP_200_OK

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """Initializes the SQLAlchemy app"""
    global app
    Recommendation.init_db(app)


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    create_logger(app).error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )
