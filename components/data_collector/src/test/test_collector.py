import unittest
import os
import sqlite3
from components.data_collector.src.main import collector

class TestCollector(unittest.TestCase):

    def setUp(self):
        if os.path.exists(collector.DB_FILE):
            os.remove(collector.DB_FILE)
        collector.init_db()

    def tearDown(self):
        if os.path.exists(collector.DB_FILE):
            os.remove(collector.DB_FILE)

    def test_init_db_creates_table(self):
        """Unit: DB schema created"""
        conn = sqlite3.connect(collector.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        table = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(table)

    def test_save_events_inserts_data(self):
        """Unit: save_events writes data to DB"""
        fake_event = [{
            "id": "evt123",
            "name": "Test Concert",
            "url": "http://example.com",
            "dates": {"start": {"localDate": "2025-10-01"}},
            "_embedded": {"venues": [{"city": {"name": "Miami"}, "state": {"stateCode": "FL"}}]}
        }]
        collector.save_events(fake_event)

        conn = sqlite3.connect(collector.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, city, state, date, url FROM events")
        row = cursor.fetchone()
        conn.close()

        self.assertEqual(row[0], "evt123")
        self.assertEqual(row[1], "Test Concert")
        self.assertEqual(row[2], "Miami")
        self.assertEqual(row[3], "FL")
        self.assertEqual(row[4], "2025-10-01")

if __name__ == "__main__":
    unittest.main()