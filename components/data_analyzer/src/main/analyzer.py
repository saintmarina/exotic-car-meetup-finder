import sqlite3

def get_sorted_events(db_file, city=None):
    """Fetch events sorted by date, optionally filtered by city"""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    if city:
        cursor.execute(
            "SELECT name, city, state, date, url FROM events WHERE city=? ORDER BY date LIMIT 20",
            (city,),
        )
    else:
        cursor.execute(
            "SELECT name, city, state, date, url FROM events ORDER BY date LIMIT 20"
        )
    rows = cursor.fetchall()
    conn.close()
    return rows