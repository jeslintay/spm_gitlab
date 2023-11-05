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

class TestCreateListing(TestRoles):
    def test_create_listing(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')
        db.session.add(l1)
        db.session.commit()

        request_body = {
            'role_name': 'Junior Engineer',
            'role_descr': 'not senior engineer',
            'skills_required': 'coding',

        }
    
    def test_negative_duplicate_role_name(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')
        l2 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')

    def test_negative_invalid_deadline(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2022-12-31')
        self.assertEqual(l1.role_deadline, '2022-12-31')



if __name__ == '__main__': 
    unittest.main()