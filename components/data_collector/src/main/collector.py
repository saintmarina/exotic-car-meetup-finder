import os
import requests
import sqlite3

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

CITY_ALIASES = {
    "la": "Los Angeles",
    "nyc": "New York",
    "new-york": "New York",
    "fort-lauderdale": "Fort Lauderdale",
    "ft-lauderdale": "Fort Lauderdale",
    "sf": "San Francisco",
}

def normalize_city(city: str) -> str:
    city = city.strip().lower().replace("-", " ")

    # apply aliases if available
    if city in CITY_ALIASES:
        return CITY_ALIASES[city]

    # otherwise just capitalize each word
    return " ".join(word.capitalize() for word in city.split())

def fetch_events(city):
    """Fetch events from Ticketmaster API for a given city"""
    city = normalize_city(city)
    print(f"Normalized city: {city}")  # DEBUG

    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "keyword": "concert",
        "city": city,
        "radius": 50,
        "unit": "miles"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("_embedded", {}).get("events", [])

def save_events(events):
    """Save fetched events into SQLite DB"""
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

def collect_for_city(city):
    """Helper to fetch and save events for a single city"""
    events = fetch_events(city)
    save_events(events)
    return events