import unittest
from applications.event-server.src.main.app import app

class TestAppIntegration(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_homepage_loads(self):
        """Integration: GET / should return 200 and include title"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Exotic Car & Concert Events in Florida", response.data)

    def test_search_city(self):
        """Integration: POST / with city input should still return 200"""
        response = self.client.post("/", data={"city": "Miami"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Events in Florida", response.data)

if __name__ == "__main__":
    unittest.main()