import unittest

from roles import Listing, Applicants, Staff, Staff_Skill, create_role_listing
from login import Accesscontrol

from datetime import datetime

class TestListing(unittest.TestCase):
    def test_to_dict(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')

        self.assertEqual(l1.to_dict(), {
            'role_name': 'Junior Engineer',
            'role_descr': 'not senior engineer',
            'skills_required': 'coding',
            'role_deadline': '2024-12-31'
            }
        )

    def test_boundary_deadline(self):

        today = datetime.today().strftime('%Y-%m-%d')
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline=today)

        self.assertEqual(l1.to_dict(), {
            'role_name': 'Junior Engineer',
            'role_descr': 'not senior engineer',
            'skills_required': 'coding',
            'role_deadline': today
            }
        )

    def test_negative_past_deadline(self):
        
            l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2020-12-31')

            output = create_role_listing(self)

            self.assertEqual(output, {
                "message": "Deadline cannot be before today."
                }
            )

    def test_negative_duplicate_role_name(self):

        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')
        l2 = Listing(role_name='Junior Engineer', role_descr='really not senior engineer', skills_required='super coding', role_deadline='2024-12-31')

        self.assertEqual(l1.to_dict(), {
            'role_name': 'Junior Engineer',
            'role_descr': 'not senior engineer',
            'skills_required': 'coding',
            'role_deadline': '2024-12-31'
            }
        )

        self.assertEqual(l2.to_dict(), {
            "message": "Role Listing already exists."
            }
        )

    
class TestApplicants(unittest.TestCase):
    def test_to_dict(self):
        a1 = Applicants(
            app_ID=1,
            Staff_ID=1,
            Staff_FName='John',
            Staff_LName='Doe',
            role_name='Junior Engineer'
        )
        
        self.assertEqual(a1.to_dict(),  
            {
            'app_ID': 1,
            'Staff_ID': 1,
            'Staff_FName': 'John',
            'Staff_LName': 'Doe',
            'role_name': 'Junior Engineer'
            }
        )


class TestStaff(unittest.TestCase):
    def test_to_dict(self):
        s1 = Staff(
            Staff_ID=130002 ,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='IT',
            Country='Singapore',
            Email='john@doe.com',
            Access_Right=1)
        
        self.assertEqual(s1.json(),  
            {
            'Staff_ID': 130002,
            'Staff_FName': 'John',
            'Staff_LName': 'Doe',
            'Dept': 'IT',
            'Country': 'Singapore',
            'Email': 'john@doe.com',
            'Access_Right': 1
            }
        )


class TestAccesscontrol(unittest.TestCase):
    def test_to_dict(self):
        a1 = Accesscontrol(
            Access_ID=99,
            Access_Control_Name='Tester'
        )
        
        self.assertEqual(a1.json(),  
            {
            'Access_ID': 99,
            'Access_Control_Name': 'Tester'
            }
        )

if __name__ == '__main__':  
    unittest.main()
    