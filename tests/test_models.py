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
from werkzeug.exceptions import NotFound

from tests.factories import RecommendationFactory


######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendationModel(unittest.TestCase):
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
        Recommendation.init_db(cls.app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        basedir = os.path.abspath(os.path.dirname(__file__))
        db.session.close()
        if os.path.exists('sqlite:///' + os.path.join(basedir, 'database.db')):
            os.remove('sqlite:///' + os.path.join(basedir, 'database.db'))

    def setUp(self):
        """ This runs before each test """
        db.session.query(Recommendation).delete()
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_rec(self):
        """It should create a Rec and assert that is exists"""
        rec = Recommendation(product_id = 1, product_name = 'foo', rec_id = 2, rec_name = 'bar', rec_type = Type.UP_SELL)
        self.assertEqual(str(rec), "<id=[None] Recommendation object for 'foo'>")
        self.assertTrue(rec is not None)
        self.assertEqual(rec.id, None)
        self.assertEqual(rec.product_id, 1)
        self.assertEqual(rec.product_name, 'foo')
        self.assertEqual(rec.rec_id, 2)
        self.assertEqual(rec.rec_name, 'bar')
        self.assertEqual(rec.rec_type, Type.UP_SELL)
        rec = Recommendation(product_id = 1, product_name = 'foo', rec_id = 2, rec_name = 'baz', rec_type = Type.CROSS_SELL)
        self.assertEqual(rec.rec_name, 'baz')
        self.assertEqual(rec.rec_type, Type.CROSS_SELL)

    def test_add_a_rec(self):
        """It should create a Rec and add it to the database"""
        recs = Recommendation.all()
        self.assertEqual(recs, [])
        rec = Recommendation(product_id = 1, product_name = 'foo', rec_id = 2, rec_name = 'bar', rec_type = Type.UP_SELL)
        self.assertTrue(rec is not None)
        self.assertEqual(rec.id, None)
        rec.create()
        self.assertIsNotNone(rec.id)
        rec = Recommendation(product_id = 1, product_name = 'foo', rec_id = 2, rec_name = 'baz', rec_type = Type.CROSS_SELL)
        recs = Recommendation.all()
        self.assertEqual(len(recs), 1)

    def test_read_a_rec(self):
        """It should Read a Rec"""
        rec = RecommendationFactory()
        logging.debug(rec)
        rec.id = None
        rec.create()
        self.assertIsNotNone(rec.id)
        found_rec = Recommendation.find(rec.id)
        self.assertEqual(found_rec.id, rec.id)
        self.assertEqual(found_rec.product_id, rec.product_id)
        self.assertEqual(found_rec.product_name, rec.product_name)
        self.assertEqual(found_rec.rec_id, rec.rec_id)
        self.assertEqual(found_rec.rec_name, rec.rec_name)
        self.assertEqual(found_rec.rec_type, rec.rec_type)

    def test_update_a_rec(self):
        """It should Update a Rec"""
        rec = RecommendationFactory()
        logging.debug(rec)
        rec.id = None
        rec.create()
        self.assertIsNotNone(rec.id)
        found_rec = Recommendation.find(rec.id)
        # Change it and save it
        rec.product_name = 'foo'
        original_id = rec.id
        rec.update()
        self.assertEqual(original_id, rec.id)
        self.assertEqual(rec.product_name, 'foo')
        # Fetch it back and make sure the id hasn't changed
        # But the data did change
        recs = Recommendation.all()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0].id, original_id)
        self.assertEqual(recs[0].product_name, 'foo')

    def test_update_no_id(self):
        """It should not Update a Rec with no id"""
        rec = RecommendationFactory()
        logging.debug(rec)
        rec.id = None
        self.assertRaises(DataValidationError, rec.update)

    def test_delete_no_id(self):
        """It should Delete a Rec"""
        rec = RecommendationFactory()
        rec.create()
        self.assertEqual(len(Recommendation.all()), 1)
        # delete the pet and make sure it isn't in the database
        rec.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_list_all_pets(self):
        """It should List all Pets in the database"""
        recs = Recommendation.all()
        self.assertEqual(len(recs), 0)
        for i in range(5):
            rec = RecommendationFactory()
            rec.create()
        recs = Recommendation.all()
        self.assertEqual(len(recs), 5)

    def test_serialize_a_pet(self):
        """It should serialize a Rec"""
        rec = Recommendation()
        data = rec.serialize()
        self.assertNotEqual(data, None)
        self.assertIn(ID, data)
        self.assertEqual(data[ID], rec.id)
        self.assertIn(PRODUCT_ID, data)
        self.assertEqual(data[PRODUCT_ID], rec.product_id)
        self.assertIn(PRODUCT_NAME, data)
        self.assertEqual(data[PRODUCT_NAME], rec.product_name)
        self.assertIn(REC_ID, data)
        self.assertEqual(data[REC_ID], rec.rec_id)
        self.assertIn(REC_NAME, data)
        self.assertEqual(data[REC_NAME], rec.rec_name)
        self.assertIn(REC_TYPE, data)
        self.assertEqual(data[REC_TYPE], rec.rec_type)

    def test_deserialize_a_pet(self):
        """It should de-serialize a Rec"""
        data = RecommendationFactory().serialize()
        rec = Recommendation()
        rec.deserialize(data)
        self.assertNotEqual(rec, None)
        self.assertEqual(rec.id, data[ID])
        self.assertEqual(rec.product_id, data[PRODUCT_ID])
        self.assertEqual(rec.product_name, data[PRODUCT_NAME])
        self.assertEqual(rec.rec_id, data[REC_ID])
        self.assertEqual(rec.rec_name, data[REC_NAME])
        self.assertEqual(rec.rec_type, data[REC_TYPE])

    def test_find_recommendation(self):
        """It should Find a Recommendation by ID"""
        recs = RecommendationFactory.create_batch(5)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        self.assertEqual(len(Recommendation.all()), 5)
        rec = Recommendation.find(recs[1].id)
        self.assertIsNotNone(rec)
        self.assertEqual(rec.id, recs[1].id)
        self.assertEqual(rec.product_id, recs[1].product_id)
        self.assertEqual(rec.product_name, recs[1].product_name)
        self.assertEqual(rec.rec_id, recs[1].rec_id)
        self.assertEqual(rec.rec_name, recs[1].rec_name)
        self.assertEqual(rec.rec_type, recs[1].rec_type)

    def test_find_recommendation_by_product_id(self):
        """It should Find a Recommendation by PRODUCT ID"""
        recs = RecommendationFactory.create_batch(5)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        product_id = recs[0].product_id
        count = len([rec for rec in recs if rec.product_id == product_id])
        found = Recommendation.find_by_product_id(product_id)
        self.assertEqual(count, 1)
        self.assertIsNotNone(found)
        self.assertEqual(recs[0].product_id, found.product_id)
    
    def test_find_recommendation_by_product_name(self):
        """It should Find a Recommendation by PRODUCT NAME"""
        recs = RecommendationFactory.create_batch(10)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        product_name = recs[0].product_name
        count = len([rec for rec in recs if rec.product_name == product_name])
        found = Recommendation.find_by_product_name(product_name)
        self.assertEqual(count, found.count())
        for rec in found:
            self.assertEqual(rec.product_name, product_name)

    def test_find_recommendation_by_rec_id(self):
        """It should Find a Recommendation by RECOMMENDATION ID"""
        recs = RecommendationFactory.create_batch(5)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        rec_id = recs[0].rec_id
        count = len([rec for rec in recs if rec.rec_id == rec_id])
        found = Recommendation.find_by_rec_id(rec_id)
        self.assertEqual(count, 1)
        self.assertIsNotNone(found)
        self.assertEqual(recs[0].rec_id, found.rec_id)
    
    def test_find_recommendation_by_rec_name(self):
        """It should Find a Recommendation by RECOMMENDATION NAME"""
        recs = RecommendationFactory.create_batch(10)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        rec_name = recs[0].rec_name
        count = len([rec for rec in recs if rec.rec_name == rec_name])
        found = Recommendation.find_by_rec_name(rec_name)
        self.assertEqual(count, found.count())
        for rec in found:
            self.assertEqual(rec.rec_name, rec_name)

    def test_find_recommendation_by_rec_type(self):
        """It should Find a Recommendation by RECOMMENDATION TYPE"""
        recs = RecommendationFactory.create_batch(10)
        for rec in recs:
            rec.create()
        logging.debug(recs)
        rec_type = recs[0].rec_type
        count = len([rec for rec in recs if rec.rec_type == rec_type])
        found = Recommendation.find_by_rec_type(rec_type)
        self.assertEqual(count, found.count())
        for rec in found:
            self.assertEqual(rec.rec_type, rec_type)
        
    def test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        recs = RecommendationFactory.create_batch(3)
        for rec in recs:
            rec.create()

        rec = Recommendation.find_or_404(recs[1].id)
        self.assertIsNot(rec, None)
        self.assertEqual(rec.id, recs[1].id)
        self.assertEqual(rec.product_id, recs[1].product_id)
        self.assertEqual(rec.product_name, recs[1].product_name)
        self.assertEqual(rec.rec_id, recs[1].rec_id)
        self.assertEqual(rec.rec_name, recs[1].rec_name)
        self.assertEqual(rec.rec_type, recs[1].rec_type)

    def test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Recommendation.find_or_404, 0)
