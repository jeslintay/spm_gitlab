import unittest

from roles import Listing

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

if __name__ == '__main__': 
    unittest.main()
    