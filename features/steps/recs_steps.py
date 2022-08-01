######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from compare import expect


@given('the following recs')
def step_impl(context):
    """ Delete all Recs and load new ones """
    # List all of the pets and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/recommendations"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for rec in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{rec['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new pets
    for row in context.table:
        payload = {
            "id": 0,
            "product_id": row['product_id'],
            "product_name": row['product_name'],
            "rec_id": row['rec_id'],
            "rec_name": row['rec_name'],
            "rec_type": row['rec_type'],
            "like_num": row['like_num']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)