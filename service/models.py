"""
Models for YourResourceModel

All of the models are stored in this module
"""
import enum
import logging

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

ID = "id"
PRODUCT_ID = "product_id"
PRODUCT_NAME = "product_name"
REC_ID = "rec_id"
REC_NAME = "rec_name"
REC_TYPE = "rec_type"

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class Type(str, enum.Enum):
    CROSS_SELL = "CROSS_SELL"
    UP_SELL = "UP_SELL"
    ACCESSORY = "ACCESSORY"
    BUY_WITH = "BUY_WITH"


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""

    pass


class Recommendation(db.Model):
    """
    Class that represents a YourResourceModel
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, unique=True, nullable=False)
    product_name = db.Column(db.String(256), nullable=False)
    rec_id = db.Column(db.Integer, unique=True, nullable=False)
    rec_name = db.Column(db.String(256), nullable=False)
    rec_type = db.Column(Enum(Type), nullable=False)

    def __repr__(self):
        return "<id=[%s] Recommendation object for %r>" % (
            self.id,
            self.product_name,
        )

    def create(self):
        """
        Creates a recommendation to the database
        """
        logger.info("Creating %s", self.product_name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a recommendation to the database
        """
        logger.info("Saving %s", self.product_name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a recommendation from the data store"""
        logger.info("Deleting %s", self.product_name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a recommendation into a dictionary"""
        return {
            ID: self.id,
            PRODUCT_ID: self.product_id,
            PRODUCT_NAME: self.product_name,
            REC_ID: self.rec_id,
            REC_NAME: self.rec_name,
            REC_TYPE: self.rec_type,
        }

    def deserialize(self, data):
        """
        Deserializes a recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the recommendation
        """
        try:
            self.id = data[ID]
            self.product_id = data[PRODUCT_ID]
            self.product_name = data[PRODUCT_NAME]
            self.rec_id = data[REC_ID]
            self.rec_name = data[REC_NAME]
            self.rec_type = data[REC_TYPE]
        except KeyError as error:
            raise DataValidationError(
                "Invalid Recommendation: missing " + error.args[0]
            )
        # except TypeError as error: // Qiheng what is this for?
        #     raise DataValidationError(
        #         "Invalid Recommendation: body of request contained bad or no data"
        #     )
        return self

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def drop_db(cls, app):
        """Initializes the database session"""
        logger.info("Dropping database")
        db.drop_all()  # drop our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the recommendation in the database"""
        logger.info("Processing all recommendation")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Recommendation by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, id: int):
        """Find a Recommendation by it's id
        :param id: the id of the Recommendation to find
        :type id: int
        :return: an instance with the id, or 404_NOT_FOUND if not found
        :rtype: Recommendation
        """
        logger.info("Processing lookup or 404 for id %s ...", id)
        return cls.query.get_or_404(id)

    @classmethod
    def find_by_product_id(cls, product_id):
        """Finds a Recommendation by it's product ID"""
        logger.info("Processing name query for %s ...", product_id)
        return cls.query.filter(cls.product_id == product_id).first_or_404()

    @classmethod
    def find_by_product_name(cls, product_name):
        """Returns all recommendation with the given product name

        Args:
            product_name (string): the product name of the recommendation you want to match
        """
        logger.info("Processing name query for %s ...", product_name)
        return cls.query.filter(cls.product_name == product_name)

    @classmethod
    def find_by_rec_id(cls, rec_id):
        """Finds a Recommendation by it's rec ID"""
        logger.info("Processing name query for %s ...", rec_id)
        return cls.query.filter(cls.rec_id == rec_id).first_or_404()

    @classmethod
    def find_by_rec_name(cls, rec_name):
        """Returns all recommendation with the given rec name

        Args:
            rec_name (string): the rec name of the recommendation you want to match
        """
        logger.info("Processing name query for %s ...", rec_name)
        return cls.query.filter(cls.rec_name == rec_name)

    @classmethod
    def find_by_rec_type(cls, rec_type):
        """Returns all recommendation with the given rec type

        Args:
            rec_type (string): the rec type of the recommendation you want to match
        """
        logger.info("Processing name query for %s ...", rec_type)
        return cls.query.filter(cls.rec_type == rec_type)
