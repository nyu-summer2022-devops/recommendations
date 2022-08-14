"""
My Service

Describe what your service does here
"""
from flask import abort, jsonify, request
from flask.logging import create_logger
from flask_restx import Resource, fields, reqparse

from service.models import Recommendation, Type

# Import Flask application
from . import app, api
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


# Define the model so that the docs reflect what can be sent
create_model = api.model('Recommendation', {

    'product_id': fields.Integer(required=True,
                                 description='The id of the product'),
    'product_name': fields.String(required=True,
                                  description='The name of the product'),
    'rec_id': fields.Integer(required=True,
                             description='The id of the recommended product'),
    'rec_name': fields.String(required=True,
                              description='The name of the recommended product'),
    'rec_type': fields.String(enum=Type._member_names_,
                              description='The type of the recommendation (e.g., cross-sell, up-sell)'),
    'like_num': fields.Integer(required=True,
                               description='The like count of the recommendation'),
})

recommendation_model = api.inherit(
    'RecommendationModel',
    create_model,
    {
        'id': fields.Integer(
            readOnly=True, description='The unique id assigned internally by service'
        ),
    }
)

# query string arguments
rec_args = reqparse.RequestParser()
rec_args.add_argument('product_id', type=str, required=False, help='List Recommendations by product_id')
rec_args.add_argument('rec_type', type=str, required=False, help='List Recommendations by rec_type')


######################################################################
#  PATH: /recommendations/{id}
######################################################################
@api.route('/recommendations/<id>')
@api.param('id', 'The Recommendation identifier')
class RecommendationResource(Resource):
    """
    RecommendationResource class

    Allows the manipulation of a single Recommendation
    GET /recommendations/{id} - Returns a Recommendation with the id
    PUT /recommendations/{id} - Update a Recommendation with the id
    DELETE /recommendations/{rec_id} -  Deletes a Recommendation with the id
    """

    # ------------------------------------------------------------------
    # RETRIEVE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc('get_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.marshal_with(recommendation_model)
    def get(self, id):
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
        return rec.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING Recommendation
    # ------------------------------------------------------------------
    @api.doc('update_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.response(400, 'The posted Recommendation data was not valid')
    @api.expect(recommendation_model)
    @api.marshal_with(recommendation_model)
    def put(self, id):
        """
        Update a Recommendation

        This endpoint will update a Recommendation based the body that is posted
        """
        create_logger(app).info("Request to update Recommendation with id: %s", id)
        rec = Recommendation.find(id)
        if not rec:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Recommendation with id '{id}' was not found.",
            )
        create_logger(app).debug('Payload = %s', api.payload)
        rec.deserialize(api.payload)
        rec.id = id
        rec.update()
        create_logger(app).info("Recommendation with ID [%s] updated.", id)
        return rec.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc('delete_recommendations')
    @api.response(204, 'Recommendation deleted')
    def delete(self, id):
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
#  PATH: /recommendations
######################################################################
@api.route('/recommendations', strict_slashes=False)
class RecommendationsCollection(Resource):
    """ Handles all interactions with collections of Recommendations """
    # ------------------------------------------------------------------
    # LIST ALL RECOMMENDATIONS
    # ------------------------------------------------------------------
    @api.doc('list_recommendations')
    @api.expect(rec_args, validate=True)
    @api.marshal_list_with(recommendation_model)
    def get(self):
        """
        Retrieves all recommendations

        This endpoint will return all the recommendations available
        """
        create_logger(app).info("Request to list all the recommendations")
        rec = []
        args = rec_args.parse_args()
        if args['product_id'] or args['rec_type']:
            rec = Recommendation.find_by_params(args['product_id'], args['rec_type'])
            if not rec:
                abort(
                    status.HTTP_404_NOT_FOUND,
                    "Recommendation was not found.",
                    )
        else:
            rec = Recommendation.all()
        message = [recommendation.serialize() for recommendation in rec]
        return message, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW RECOMMENDATION
    # ------------------------------------------------------------------
    @api.doc('create_recommendations')
    @api.response(400, 'The posted data was not valid')
    @api.expect(recommendation_model)
    @api.marshal_with(recommendation_model, code=201)
    def post(self):
        """
        Creates a Recommendation
        This endpoint will create a Recommendation based the data in the body this is posted
        """
        create_logger(app).info("Request to create a Recommendation")
        rec = Recommendation()
        create_logger(app).debug('Payload = %s', api.payload)
        rec.deserialize(api.payload)
        rec.create()
        create_logger(app).info("Recommendation with new id [%s] created!", rec.id)
        location_url = api.url_for(RecommendationResource, id=rec.id, _external=True)
        return rec.serialize(), status.HTTP_201_CREATED,  {'Location': location_url}


######################################################################
#  PATH: /recommendations/{id}/like
######################################################################
@api.route('/recommendations/<id>/like')
@api.param('id', 'The Recommendation identifier')
class LikeResource(Resource):
    """ Like actions on a Recommendation """
    @api.doc('like_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.response(409, 'The Recommendation is not available for like')
    def put(self, id):
        """
        Like a Recommendation

        This endpoint will like a Recommendation based on the id
        """
        create_logger(app).info("Request to like Recommendation with id: %s", id)
        rec = Recommendation.find(id)
        if not rec:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Recommendation with id '{id}' was not found.",
            )
        rec.like_num += 1
        rec.update()

        create_logger(app).info("Recommendation with ID [%s] is liked.", rec.id)
        return rec.serialize(), status.HTTP_200_OK


######################################################################
#  PATH: /recommendations/{id}/unlike
######################################################################
@api.route('/recommendations/<id>/unlike')
@api.param('id', 'The Recommendation identifier')
class UnlikeResource(Resource):
    """ Unlike actions on a Recommendation """
    @api.doc('unlike_recommendations')
    @api.response(404, 'Recommendation not found')
    @api.response(409, 'The Recommendation is not available for unlike')
    def put(self, id):
        """
        Unlike a Recommendation

        This endpoint will unlike a Recommendation based on the id
        """
        create_logger(app).info("Request to unlike Recommendation with id: %s", id)
        rec = Recommendation.find(id)
        if not rec:
            abort(
                status.HTTP_404_NOT_FOUND,
                f"Recommendation with id '{id}' was not found.",
            )

        if rec.like_num >= 1:
            rec.like_num -= 1
        rec.update()

        create_logger(app).info("Recommendation with ID [%s] is unliked.", rec.id)
        return rec.serialize(), status.HTTP_200_OK


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


# ######################################################################
# # ADD A NEW RECOMMENDATION
# ######################################################################
# @app.route("/recommendations", methods=["POST"])
# def create_recommendations():
#     """
#     Creates a Recommendation
#     This endpoint will create a Recommendation based the data in the body this is posted
#     """
#     create_logger(app).info("Request to create a rec")
#     check_content_type("application/json")
#     rec = Recommendation()
#     create_logger(app).info(request.get_json())
#     rec.deserialize(request.get_json())
#     rec.create()
#     message = rec.serialize()
#     location_url = url_for("get_recommendations", id=rec.id, _external=True)
#     resp = make_response(jsonify(message), status.HTTP_201_CREATED)
#     resp.headers["Location"] = location_url
#     return resp


# ######################################################################
# # Read A Recommendation
# ######################################################################
# @app.route("/recommendations/<int:id>", methods=["GET"])
# def get_recommendations(id):
#     """
#     Retrieve a single Recommendation

#     This endpoint will return a Recommendation based on it's id
#     """
#     create_logger(app).info("Request for Recommendation with id: %s", id)
#     rec = Recommendation.find(id)
#     if not rec:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id '{id}' was not found.",
#         )

#     create_logger(app).info("Returning recommendation: %s", rec.product_name)
#     return jsonify(rec.serialize()), status.HTTP_200_OK


# ######################################################################
# # List all the Recommendations
# ######################################################################
# @app.route("/recommendations", methods=["GET"])
# def list_recommendations():
#     """
#     Retrieves all recommendations

#     This endpoint will return all the recommendations available
#     """
#     create_logger(app).info("Request to list all the recommendations")

#     rec = []
#     product_id = request.args.get('product_id')
#     rec_type = request.args.get('rec_type')
#     if product_id or rec_type:
#         rec = Recommendation.find_by_params(product_id, rec_type)
#         if not rec:
#             abort(
#                 status.HTTP_404_NOT_FOUND,
#                 "Recommendation was not found.",
#                 )
#     else:
#         rec = Recommendation.all()
#     message = [recommendation.serialize() for recommendation in rec]
#     return jsonify(message), status.HTTP_200_OK


# ######################################################################
# # UPDATE AN EXISTING RECOMMENDATION
# ######################################################################
# @app.route("/recommendations/<int:id>", methods=["PUT"])
# def update_recommendations(id):
#     """
#     Update a Recommendation

#     This endpoint will update a Recommendation based the body that is posted
#     """
#     create_logger(app).info("Request to update Recommendation with id: %s", id)
#     check_content_type("application/json")

#     rec = Recommendation.find(id)
#     if not rec:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id '{id}' was not found.",
#         )

#     rec.deserialize(request.get_json())
#     rec.id = id
#     rec.update()

#     create_logger(app).info("Recommendation with ID [%s] updated.", rec.id)
#     return jsonify(rec.serialize()), status.HTTP_200_OK


# ######################################################################
# # DELETE A RECOMMENDATION
# ######################################################################
# @app.route("/recommendations/<int:id>", methods=["DELETE"])
# def delete_recommendations(id):
#     """
#     Delete a Recommendation
#     This endpoint will delete a Recommendation based the id specified in the path
#     """
#     create_logger(app).info("Request to delete recommendation with id: %s", id)
#     rec = Recommendation.find(id)
#     if rec:
#         rec.delete()

#     create_logger(app).info("Recommendation with ID [%s] delete complete.", id)
#     return "", status.HTTP_204_NO_CONTENT


# ######################################################################
# # Like A RECOMMENDATION
# ######################################################################
# @app.route("/recommendations/<int:id>/like", methods=["PUT"])
# def like_recommendations(id):
#     """
#     Like a Recommendation

#     This endpoint will like a Recommendation based on the id
#     """
#     create_logger(app).info("Request to like Recommendation with id: %s", id)
#     check_content_type("application/json")

#     rec = Recommendation.find(id)
#     if not rec:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id '{id}' was not found.",
#         )

#     rec.deserialize(request.get_json())
#     rec.id = id
#     rec.like_num += 1
#     rec.update()

#     create_logger(app).info("Recommendation with ID [%s] is liked.", rec.id)
#     return jsonify(rec.serialize()), status.HTTP_200_OK


# ######################################################################
# # Unlike A RECOMMENDATION
# ######################################################################
# @app.route("/recommendations/<int:id>/unlike", methods=["PUT"])
# def unlike_recommendations(id):
#     """
#     Unlike a Recommendation

#     This endpoint will unlike a Recommendation based on the id
#     """
#     create_logger(app).info("Request to unlike Recommendation with id: %s", id)
#     check_content_type("application/json")

#     rec = Recommendation.find(id)
#     if not rec:
#         abort(
#             status.HTTP_404_NOT_FOUND,
#             f"Recommendation with id '{id}' was not found.",
#         )

#     rec.deserialize(request.get_json())
#     rec.id = id

#     if rec.like_num >= 1:
#         rec.like_num -= 1
#     rec.update()

#     create_logger(app).info("Recommendation with ID [%s] is unliked.", rec.id)
#     return jsonify(rec.serialize()), status.HTTP_200_OK

# ######################################################################
# #  U T I L I T Y   F U N C T I O N S
# ######################################################################


# def init_db():
#     """Initializes the SQLAlchemy app"""
#     global app
#     Recommendation.init_db(app)


# def check_content_type(media_type):
#     """Checks that the media type is correct"""
#     content_type = request.headers.get("Content-Type")
#     if content_type and content_type == media_type:
#         return
#     create_logger(app).error("Invalid Content-Type: %s", content_type)
#     abort(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         "Content-Type must be {}".format(media_type),
#     )
