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

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_rec = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_rec.serialize())
        response = self.client.post(
            BASE_URL,
            json=test_rec.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_rec = response.get_json()
        self.assertEqual(new_rec[PRODUCT_ID], test_rec.product_id)
        self.assertEqual(new_rec[PRODUCT_NAME], test_rec.product_name)
        self.assertEqual(new_rec[REC_ID], test_rec.rec_id)
        self.assertEqual(new_rec[REC_NAME], test_rec.rec_name)
        self.assertEqual(new_rec[REC_TYPE], test_rec.rec_type)

        # Check that the location header was correct
        response = self.client.get(location, content_type=CONTENT_TYPE_JSON)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_rec = response.get_json()
        self.assertEqual(new_rec[PRODUCT_ID], test_rec.product_id)
        self.assertEqual(new_rec[PRODUCT_NAME], test_rec.product_name)
        self.assertEqual(new_rec[REC_ID], test_rec.rec_id)
        self.assertEqual(new_rec[REC_NAME], test_rec.rec_name)
        self.assertEqual(new_rec[REC_TYPE], test_rec.rec_type)

    def test_get_recommendation(self):
        """It should Get a single Recommendation"""
        # get the id of a recommendation
        test_rec = self._create_recommendations(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_rec.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["product_name"], test_rec.product_name)

    def test_get_recommendation_not_found(self):
        """It should not Get a Recommendation thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_list_recommendation(self):
        """It should get all the Recommendations"""
        # create recommendations
        test_rec = self._create_recommendations(3)[0]
        response = self.client.get(f"{BASE_URL}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data[0]["product_name"], test_rec.product_name)

    def test_update_recommendation(self):
        """It should Update an existing Recommendation"""
        # create a recommendation to update
        test_rec = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_rec.serialize())
        response = self.client.post(
            BASE_URL,
            json=test_rec.serialize(),
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

        # # # create a recommendation to update
        # test_rec = self._create_recommendations(1)[0]
        # logging.debug("Test Recommendation: %s", test_rec.serialize())
        
        # update the recommendation
        new_rec = response.get_json()
        new_rec[PRODUCT_NAME] = "Hat"
        new_rec[PRODUCT_ID] = 100
        logging.debug("New Recommendation: %s", new_rec)
        response = self.client.put(
            f"{BASE_URL}/{new_rec[ID]}",
            json=new_rec,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_recommendation = response.get_json()
        self.assertEqual(updated_recommendation[ID], new_rec[ID])
        self.assertEqual(updated_recommendation[PRODUCT_ID], 100)
        self.assertEqual(updated_recommendation[PRODUCT_NAME], "Hat")

        response2 = self.client.put(
            f"{BASE_URL}/99999",  #non-existing id
            json=new_rec,
            content_type=CONTENT_TYPE_JSON,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_recommendation_with_id(self):
        """It should return 405 method not allowed error"""
        response = self.client.post(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("405 Method Not Allowed", data["message"])
    
    def test_create_recommendation_no_data(self):
        """It should not Create a Recommendation with missing data"""
        response = self.client.post(
            BASE_URL,
            json={},
            content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recommendation_no_content_type(self):
        """It should not Create a Recommendation with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    # def test_create_recommendation_id(self):
    #     """It should not Create a Recommendation with bad id data"""
    #     test_rec = RecommendationFactory()
    #     logging.debug(test_rec)
    #     # change available to a string
    #     test_rec.id = "0"
    #     response = self.client.post(
    #         BASE_URL,
    #         json=test_rec.serialize(),
    #         content_type=CONTENT_TYPE_JSON
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_create_recommendation_bad_rec_type(self):
    #     """It should not Create a Recommendation with bad rec_type data"""
    #     recommendation = RecommendationFactory()
    #     logging.debug(recommendation)
    #     # change rec_type to a bad string
    #     test_rec = recommendation.serialize()
    #     test_rec[REC_TYPE] = "aaaaa"    # wrong case
    #     response = self.client.post(
    #         BASE_URL,
    #         json=test_rec,
    #         content_type=CONTENT_TYPE_JSON
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_a_recommendation(self):
        """ It should delete a recommendation """
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

    def test_deserialize_missing_data(self):
        """It should not deserialize a Recommendation with missing data"""
        data = {"id": 1, "product_id": "toys", "rec_id": 123}
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        rec = Recommendation()
        self.assertRaises(DataValidationError, rec.deserialize, data)

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
