"""
Test cases for YourResourceModel Model

"""
import logging
import os
import unittest

from flask import Flask
from service.models import DataValidationError, Recommendation, Type, db


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
    #  T E S T   C A S E S
    ######################################################################

    def test_XXXX(self):
        """ It should always be true """
        self.assertTrue(True)

    def test_db_empty(self):
        """ Database init should contain empty rows """
        query = Recommendation.all()
        self.assertEqual(len(query), 0)

    def test_recommendation_create(self):
        """ Create recommendation db should contain one row """
        rec = Recommendation()
        Recommendation.create(rec, 1, 'foo', 2, 'bar', Type.UP_SELL)
        query = Recommendation.all()
        res = {'id': 1, 'product_id': 1, 'product_name': 'foo', 'rec_id': 2, 'rec_name': 'bar', 'rec_type': Type.UP_SELL}
        self.assertEqual(query[0].serialize(), res)
