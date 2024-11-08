import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """
        Set up test client before each test method.
        This allows us to simulate HTTP requests to our Flask app.
        """
        self.client = app.test_client()
        self.client.testing = True

    def test_home_route(self):
        """
        Test the home route ('/') to ensure it returns the correct response.
        """
        # Send a GET request to the home route
        response = self.client.get('/')

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        data = response.get_json()

        # Check that the response contains the expected message
        self.assertEqual(
            data, 
            {"message": "Hello level 400 FET, Quality Assurance!"}
        )

if __name__ == '__main__':
    unittest.main()


