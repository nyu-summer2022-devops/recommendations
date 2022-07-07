"""
Recommendation API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import logging
import os
from unittest import TestCase

from service import app
from service.models import (
    ID,
    PRODUCT_ID,
    PRODUCT_NAME,
    REC_ID,
    REC_NAME,
    REC_TYPE,
    Recommendation,
    db,
)
from service.routes import init_db
from service.utils import status  # HTTP Status Codes

from tests.factories import RecommendationFactory

BASE_URL = "/recommendations"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "database.db"
        )
        app.logger.setLevel(logging.CRITICAL)
        init_db()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        basedir = os.path.abspath(os.path.dirname(__file__))
        db.session.close()
        if os.path.exists("sqlite:///" + os.path.join(basedir, "database.db")):
            os.remove("sqlite:///" + os.path.join(basedir, "database.db"))

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Recommendation).delete()
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_recommendations(self, count):
        """Factory method to create recommendations in bulk"""
        recommendations = []
        for _ in range(count):
            test_rec = RecommendationFactory()
            response = self.client.post(
                BASE_URL,
                json=test_rec.serialize(),
                content_type=CONTENT_TYPE_JSON,
            )
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test recommendation",
            )
            new_rec = response.get_json()
            test_rec.id = new_rec["id"]
            recommendations.append(test_rec)
        return recommendations

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_recommendation(self):
        """It should Create a new Recommendation"""
        test_rec = RecommendationFactory()
        logging.debug("Test Recommendation: %s", test_rec.serialize())
        response = self.client.post(
            BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
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
            BASE_URL, json=test_rec.serialize(), content_type=CONTENT_TYPE_JSON
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

        # response2 = self.client.put( // Sean
        #     f"{BASE_URL}/99999",  # non-existing id
        #     json=new_rec,
        #     content_type=CONTENT_TYPE_JSON,
        # )
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_recommendation(self):
        """It should Delete a Recommendation"""
        # create a recommendation to update
        test_rec = self._create_recommendations(1)[0]
        # delete the recommendation

        response = self.client.delete(f"{BASE_URL}/{test_rec.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # try to read the deleted recommendation
        response = self.client.get(f"{BASE_URL}/{test_rec.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recommendation_with_id(self):
        """It should return 405 method not allowed error"""
        response = self.client.post(f"{BASE_URL}/0")
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("405 Method Not Allowed", data["message"])

    def test_create_recommendation_no_data(self):
        """It should not Create a Recommendation with missing data"""
        response = self.client.post(
            BASE_URL, json={}, content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_recommendation_no_content_type(self):
        """It should not Create a Recommendation with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(
            response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        )

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
