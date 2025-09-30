import os
import requests
import sqlite3
from flask import Flask, render_template_string

app = Flask(__name__)

API_KEY = os.getenv("TICKETMASTER_API_KEY", "9AUPkJGAHLnkIpTbHw7xdjbeOD2Spusb")

DB_FILE = "events.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT,
        state TEXT,
        date TEXT,
        url TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()


def fetch_events(city):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "keyword": "concert",
        "city": city,
        "stateCode": "FL",
        "radius": 50,
        "unit": "miles"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("_embedded", {}).get("events", [])


def save_events(events):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for e in events:
        event_id = e["id"]
        name = e["name"]
        city = e["_embedded"]["venues"][0]["city"]["name"]
        state = e["_embedded"]["venues"][0]["state"]["stateCode"]
        date = e["dates"]["start"].get("localDate", "")
        url = e["url"]
        cursor.execute("""
        INSERT OR IGNORE INTO events (id, name, city, state, date, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (event_id, name, city, state, date, url))
    conn.commit()
    conn.close()


@app.route("/")
def index():
    cities = ["Miami", "Fort Lauderdale", "Boca Raton", "Palm Beach", "Kendall"]
    all_events = []

    for city in cities:
        try:
            events = fetch_events(city)
            save_events(events)
            all_events.extend(events)
        except Exception as e:
            print(f"Error fetching {city}: {e}")

    # Render events from DB
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, city, state, date, url FROM events ORDER BY date LIMIT 20")
    rows = cursor.fetchall()
    conn.close()

    template = """
    <h1>Exotic Car & Concert Events in Florida</h1>
    {% if rows %}
      <ul>
      {% for name, city, state, date, url in rows %}
        <li>
          <b>{{ name }}</b> - {{ city }}, {{ state }} on {{ date }}
          (<a href="{{ url }}" target="_blank">Details</a>)
        </li>
      {% endfor %}
      </ul>
    {% else %}
      <p>No events found.</p>
    {% endif %}
    """
    return render_template_string(template, rows=rows)


if __name__ == "__main__":
    app.run(debug=True)