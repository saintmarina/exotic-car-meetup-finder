import unittest
import os
import sqlite3
from components.data_analyzer.src.main import analyzer
from components.data_collector.src.main import collector

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        if os.path.exists(collector.DB_FILE):
            os.remove(collector.DB_FILE)
        collector.init_db()

        # Insert sample events
        conn = sqlite3.connect(collector.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", 
                       ("evt1", "Event 1", "Miami", "FL", "2025-10-01", "http://event1.com"))
        cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?)", 
                       ("evt2", "Event 2", "Boca Raton", "FL", "2025-09-25", "http://event2.com"))
        conn.commit()
        conn.close()

    def tearDown(self):
        if os.path.exists(collector.DB_FILE):
            os.remove(collector.DB_FILE)

    def test_get_events_sorted(self):
        """Unit: Analyzer returns sorted events by date"""
        rows = analyzer.get_events(limit=2)
        self.assertEqual(len(rows), 2)
        # Check that sorting is ascending by date
        self.assertLessEqual(rows[0][3], rows[1][3])

if __name__ == "__main__":
    unittest.main()