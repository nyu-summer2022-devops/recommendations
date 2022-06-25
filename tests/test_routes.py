"""
Recommendation API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import json
import logging
import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

from service import app
from service.models import (PRODUCT_ID, PRODUCT_NAME, REC_ID, REC_NAME,
                            REC_TYPE, Recommendation, db)
from service.routes import init_db
from service.utils import status  # HTTP Status Codes

from tests.factories import RecommendationFactory

BASE_URL = "/recommendations"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        basedir = os.path.abspath(os.path.dirname(__file__))
        db.session.close()
        if os.path.exists('sqlite:///' + os.path.join(basedir, 'database.db')):
            os.remove('sqlite:///' + os.path.join(basedir, 'database.db'))

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Recommendation).delete()
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_rec = RecommendationFactory()
            response = self.client.post(
                BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_rec = response.get_json()
            test_rec.id = new_rec["id"]
            recommendations.append(test_rec)
        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
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
