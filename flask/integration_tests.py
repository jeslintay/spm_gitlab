import unittest
import flask_testing
import json
from roles import app, db, Listing, Applicants, Staff, Staff_Skill


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

class TestGetSkills(TestRoles):
    def test_get_skills(self):
        s1 = Staff(
            Staff_ID=130002 ,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='IT',
            Country='Singapore',
        )
        sk1 = Staff_Skill(
            Staff_ID=130002,
            Skill_Name='Python',
        )
        db.session.add(s1)
        db.session.commit()

        request_body = {
            

        }
    
    


if __name__ == '__main__': 
    unittest.main()