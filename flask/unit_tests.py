import unittest

from roles import Listing, Applicants, Staff
from login import Accesscontrol

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
            Staff_ID=1,
            Staff_FName='John',
            Staff_LName='Doe',
            Dept='IT',
            Country='Singapore',
            Email='john@doe.com',
            AccessRights=1)
        
        self.assertEqual(s1.to_dict(),  
            {
            'Staff_ID': 0,
            'Staff_FName': 'John',
            'Staff_LName': 'Doe',
            'Dept': 'IT',
            'Country': 'Singapore',
            'Email': 'john@doe.com',
            'AccessRights': 1
            }
        )

class TestAccesscontrol(unittest.TestCase):
    def test_to_dict(self):
        a1 = Accesscontrol(
            Access_ID=99,
            Access_Control_Name='Tester'
        )
        
        self.assertEqual(a1.to_dict(),  
            {
            'Access_ID': 99,
            'Access_Control_Name': 'Tester'
            }
        )

if __name__ == '__main__':  
    unittest.main()
    