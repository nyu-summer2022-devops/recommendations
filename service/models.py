"""
Models for YourResourceModel

All of the models are stored in this module
"""
import enum
import logging

import idna
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

ID = 'id'
PRODUCT_ID = 'product_id'
PRODUCT_NAME = 'product_name'
REC_ID = 'rec_id'
REC_NAME = 'rec_name'
REC_TYPE = 'rec_type'

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class Type(enum.Enum):
    CROSS_SELL = 0
    UP_SELL    = 1
    ACCESSORY  = 2
    BUY_WITH   = 3

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

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
        return "<id=[%s] Recommendation object for %r>" % (self.id, self.product_name)

    def create(self, product_id, product_name, rec_id, rec_name, rec_type):
        """
        Creates a recommendation to the database
        """
        logger.info("Creating %s", self.product_name)
        self.id = None  # id must be none to generate next primary key
        self.product_id = product_id
        self.product_name = product_name
        self.rec_id = rec_id
        self.rec_name = rec_name
        self.rec_type = rec_type
        db.session.add(self)
        db.session.commit()

    def update(self):
        # TODO
        """
        Updates a YourResourceModel to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        # TODO
        """ Removes a YourResourceModel from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a recommendation into a dictionary """
        return {
            ID: self.id, 
            PRODUCT_ID: self.product_id, 
            PRODUCT_NAME: self.product_name, 
            REC_ID: self.rec_id, 
            REC_NAME: self.rec_name, 
            REC_TYPE: self.rec_type
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
                "Invalid YourResourceModel: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid YourResourceModel: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables
    
    @classmethod
    def drop_db(cls, app):
        """ Initializes the database session """
        logger.info("Dropping database")
        db.drop_all()  # drop our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the recommendation in the database """
        logger.info("Processing all recommendation")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a YourResourceModel by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        # TODO
        """Returns all recommendation with the given name

        Args:
            name (string): the name of the recommendation you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
