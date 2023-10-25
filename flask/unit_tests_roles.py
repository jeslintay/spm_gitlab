import unittest

from roles import Listing
from login import Staff, Accesscontrol

class TestListing(unittest.TestCase):
    def test_to_dict(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')

        self.assertEqual(l1.to_dict(), {
            'id': None,
            'role_name': 'Junior Engineer',
            'role_descr': 'not senior engineer',
            'skills_required': 'coding',
            'role_deadline': '2024-12-31'
            }
        )

'''
    def test_create_role_listing(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')
        self.assertEqual(l1.role_deadline, '2024-12-31')

    def test_negative_duplicate_role_name(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')
        l2 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2024-12-31')

    def test_negative_invalid_deadline(self):
        l1 = Listing(role_name='Junior Engineer', role_descr='not senior engineer', skills_required='coding', role_deadline='2022-12-31')
        self.assertEqual(l1.role_deadline, '2022-12-31')

'''



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
    