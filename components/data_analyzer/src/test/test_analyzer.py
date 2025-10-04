import unittest
import sqlite3
import os
from components.data_analyzer.src.main.analyzer import get_sorted_events

DB_FILE = "test_events.db"

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        """Reset test DB and insert fake events."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            state TEXT,
            date TEXT,
            url TEXT
        )
        """)
        fake_events = [
            ("evt1", "Concert A", "Miami", "FL", "2025-12-01", "http://a.com"),
            ("evt2", "Concert B", "Miami", "FL", "2025-11-01", "http://b.com"),
            ("evt3", "Concert C", "Boston", "MA", "2025-10-01", "http://c.com"),
        ]
        cursor.executemany("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", fake_events)
        conn.commit()
        conn.close()

    def tearDown(self):
        """Remove DB after each test."""
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    def test_sorted_events_no_city(self):
        """Should return all events sorted by date (ascending)."""
        rows = get_sorted_events(DB_FILE)
        self.assertEqual(len(rows), 3)
        # Check sorting
        self.assertEqual(rows[0][3], "2025-10-01")
        self.assertEqual(rows[1][3], "2025-11-01")
        self.assertEqual(rows[2][3], "2025-12-01")

    def test_sorted_events_with_city(self):
        """Should return only events for given city, sorted by date."""
        rows = get_sorted_events(DB_FILE, city="Miami")
        self.assertEqual(len(rows), 2)
        # Both rows should be Miami
        for row in rows:
            self.assertEqual(row[1], "Miami")
        # Check sorting for Miami subset
        self.assertEqual(rows[0][3], "2025-11-01")
        self.assertEqual(rows[1][3], "2025-12-01")

if __name__ == "__main__":
    unittest.main()