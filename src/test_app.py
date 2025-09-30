import os
import sqlite3
import unittest
from app import app, init_db, save_events, DB_FILE

class TestApp(unittest.TestCase):

    def setUp(self):
        """Runs before each test — reset DB to empty"""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
        init_db()
        self.client = app.test_client()

    def tearDown(self):
        """Clean up DB after tests"""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    def test_save_events_unit(self):
        """Unit test: save_events inserts into DB"""
        fake_events = [
            {
                "id": "evt123",
                "name": "Test Event",
                "url": "http://example.com",
                "dates": {"start": {"localDate": "2025-10-01"}},
                "_embedded": {
                    "venues": [
                        {"city": {"name": "Miami"}, "state": {"stateCode": "FL"}}
                    ]
                }
            }
        ]

        save_events(fake_events)

        # Query DB directly
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, city, state, date, url FROM events")
        row = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "evt123")
        self.assertEqual(row[1], "Test Event")
        self.assertEqual(row[2], "Miami")
        self.assertEqual(row[3], "FL")
        self.assertEqual(row[4], "2025-10-01")

    def test_index_integration(self):
        """Integration test: hitting / returns HTML"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Events in Florida", response.data)


if __name__ == "__main__":
    unittest.main()