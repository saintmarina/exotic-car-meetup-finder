import unittest
import os
import sqlite3
from unittest.mock import patch, MagicMock

from components.data_collector.src.main import collector

TEST_DB_FILE = "test_events.db"


class TestCollector(unittest.TestCase):

    def setUp(self):
        # Override DB_FILE for testing
        collector.DB_FILE = TEST_DB_FILE

        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
        collector.init_db()

    def tearDown(self):
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)

    def test_normalize_city_basic(self):
        """Normalize single and multi-word cities correctly"""
        self.assertEqual(collector.normalize_city("miami"), "Miami")
        self.assertEqual(collector.normalize_city("los angeles"), "Los Angeles")

    def test_normalize_city_alias(self):
        """Normalize using city aliases"""
        self.assertEqual(collector.normalize_city("nyc"), "New York")
        self.assertEqual(collector.normalize_city("fort-lauderdale"), "Fort Lauderdale")
        self.assertEqual(collector.normalize_city("sf"), "San Francisco")

    def test_save_events(self):
        """Saving events inserts them into DB"""
        fake_events = [
            {
                "id": "evt1",
                "name": "Test Concert",
                "url": "http://example.com",
                "dates": {"start": {"localDate": "2025-12-01"}},
                "_embedded": {"venues": [{"city": {"name": "Miami"}, "state": {"stateCode": "FL"}}]},
            }
        ]
        collector.save_events(fake_events)

        conn = sqlite3.connect(TEST_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, city, state, date, url FROM events")
        row = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(row)
        self.assertEqual(row[0], "evt1")
        self.assertEqual(row[1], "Test Concert")
        self.assertEqual(row[2], "Miami")
        self.assertEqual(row[3], "FL")
        self.assertEqual(row[4], "2025-12-01")

    @patch("components.data_collector.src.main.collector.requests.get")
    def test_collect_for_city_with_mock(self, mock_get):
        """collect_for_city should fetch and save events using mocked API"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "_embedded": {
                "events": [
                    {
                        "id": "evt2",
                        "name": "Mocked Concert",
                        "url": "http://mock.com",
                        "dates": {"start": {"localDate": "2025-11-15"}},
                        "_embedded": {"venues": [{"city": {"name": "Boston"}, "state": {"stateCode": "MA"}}]},
                    }
                ]
            }
        }
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        events = collector.collect_for_city("Boston")

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["name"], "Mocked Concert")

        # Check it was written to DB
        conn = sqlite3.connect(TEST_DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name, city FROM events WHERE id=?", ("evt2",))
        row = cursor.fetchone()
        conn.close()

        self.assertEqual(row[0], "Mocked Concert")
        self.assertEqual(row[1], "Boston")


if __name__ == "__main__":
    unittest.main()