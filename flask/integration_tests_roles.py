import unittest
import flask_testing
import json
from roles import app, Listing


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
            
        }
        

if __name__ == '__main__': 
    unittest.main()