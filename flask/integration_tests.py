import unittest
from flask import Flask, request, jsonify
from flask_cors import CORS
import flask_testing
import json
from roles import db, Listing, Applicants, Staff, validate_role_listing
from login import Accesscontrol
from datetime import datetime

app = Flask(__name__)
CORS(app)

class TestRoles(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestRoles(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + \
                                        'root:' + \
                                        '@localhost:3306/sbrp'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                            'pool_recycle': 280}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestApplyRole(TestRoles):
    def test_apply_role(self):

        s1 = Staff(Staff_ID=130002, Staff_FName='John', Staff_LName='Doe', Dept='IT', Country='Singapore', Email='john@it.com', Access_Right=1)

        l1 = Listing(role_name='Tester', role_descr='Test software', skills_required='Python', role_deadline='2024-12-31')

        db.session.add(s1)
        db.session.add(l1)
        db.session.commit()

        request_body = {
            "Staff_ID": 130002,
            "Staff_FName": "John",
            "Staff_LName": "Doe",
            "role_name": "Tester"
        }

        response = self.client.post("/apply_role", data=json.dumps(request_body))
        self.assertEqual(response.json, {
            "app_ID": 1, # autoincrement
            "Staff_ID": 130002,
            "Staff_FName": "John",
            "Staff_LName": "Doe",
            "role_name": "Tester"})



#if __name__ == '__main__': 
  #  unittest.main()