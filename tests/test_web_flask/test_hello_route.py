import unittest
import requests

class TestHelloRoute(unittest.TestCase):
    def test_index_route(self):
        # Create a client to connect to the server
        response = requests.get('http://127.0.0.1:5000/')
        
        # Check that the response is correct
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello HBNB!')
    

if __name__ == '__main__':
    unittest.main()
