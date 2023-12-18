import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the App', response.data)

    def test_check_relevance_route(self):
        # Add more tests for your routes
        pass

if __name__ == '__main__':
    unittest.main()
