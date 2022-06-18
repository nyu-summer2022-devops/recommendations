"""
Test cases for YourResourceModel Model

"""
import logging
import os
import unittest

from flask import Flask
from service.models import (ID, PRODUCT_ID, PRODUCT_NAME, REC_ID, REC_NAME,
                            REC_TYPE, DataValidationError, Recommendation,
                            Type, db)


######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendation(unittest.TestCase):
    """ Test Cases for Recommendation Model """
    app = None

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        basedir = os.path.abspath(os.path.dirname(__file__))
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
        cls.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        Recommendation.init_db(self.app)

    def tearDown(self):
        """ This runs after each test """
        Recommendation.drop_db(self.app)

    ######################################################################
    #  U T I L I T Y
    ######################################################################

    def create_dummy(self):
        rec = Recommendation()
        Recommendation.create(rec, 1, 'foo', 2, 'bar', Type.UP_SELL)

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ It should always be true """
        self.assertTrue(True)

    def test_db_empty(self):
        """ Database init should contain empty rows """
        query = Recommendation.all()
        self.assertEqual(len(query), 0)
    
    def test_recommendation_find(self):
        """ Find should work"""
        self.create_dummy()
        query = Recommendation.find(1)
        self.assertEqual(query.serialize()[ID], 1)

    def test_recommendation_find_by_product_id(self):
        """ Find product id should work"""
        self.create_dummy()
        query = Recommendation.find_by_product_id(1)
        self.assertEqual(query.serialize()[PRODUCT_ID], 1)

    def test_recommendation_find_by_product_name(self):
        """ Find product name should work"""
        self.create_dummy()
        query = Recommendation.find_by_product_name('foo')
        self.assertEqual(query[0].serialize()[PRODUCT_ID], 1)

    def test_recommendation_create(self):
        """ Create recommendation and db should contain only one row """
        self.create_dummy()
        query = Recommendation.find(1)
        res = {ID: 1, PRODUCT_ID: 1, PRODUCT_NAME: 'foo', REC_ID: 2, REC_NAME: 'bar', REC_TYPE: Type.UP_SELL}
        self.assertEqual(query.serialize(), res)

    def test_recommendation_update(self):
        """ Update recommendation db """
        self.create_dummy()
        query = Recommendation.find(1)
        query.deserialize({**query.serialize(), PRODUCT_NAME: 'baz'})
        query.update()
        query = Recommendation.find(1)
        res = {ID: 1, PRODUCT_ID: 1, PRODUCT_NAME: 'baz', REC_ID: 2, REC_NAME: 'bar', REC_TYPE: Type.UP_SELL}
        self.assertEqual(query.serialize(), res)

    def test_recommendation_delete(self):
        """ Delete recommendation db """
        self.create_dummy()
        query = Recommendation.find(1)
        query.delete()
        self.assertEqual(len(Recommendation.all()), 0)
