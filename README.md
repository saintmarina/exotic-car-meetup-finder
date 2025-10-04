# 🎟️ Ticketmaster Event Finder

This project is a simple **Flask application** that fetches live event data from the [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/), stores it in a local SQLite database, and provides a web interface to search and analyze events by city.  

It was built as a course project to demonstrate:
- Fetching and normalizing data from an external API
- Storing and querying data from a relational database
- Performing simple analysis (sorting by date, filtering by city)
- Writing unit and integration tests for key components

---

## 📂 Project Structure
ticket-master-project/
├── applications/
│   └── event-server/
│       └── src/
│           └── main/
│               └── app.py            # Flask web server
├── components/
│   ├── data_collector/
│   │   └── src/
│   │       ├── main/
│   │       │   └── collector.py      # Fetch & save events
│   │       └── test/
│   │           └── test_collector.py # Unit tests for collector
│   └── data_analyzer/
│       └── src/
│           ├── main/
│           │   └── analyzer.py       # Query & sort events
│           └── test/
│               └── test_analyzer.py  # Unit tests for analyzer
├── requirements.txt
├── Procfile
└── README.md

---

## ⚙️ Setup & Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd ticket-master-project
    ```
2.	Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate 
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.	Set your Ticketmaster API Key (replace YOUR_KEY_HERE with your key):
    ```bash
    export TICKETMASTER_API_KEY=YOUR_KEY_HERE
    ```

## Running the App Locally
    ```bash
    export PYTHONPATH=.
    flask --app applications/event-server/src/main/app run
    ```

Then open http://127.0.0.1:5000 in your browser.
	•	By default, the homepage loads events from predefined Florida cities.
	•	You can also search by city using the input field.
	•	Events are stored in SQLite (events.db) and sorted by date.

## 🧪 Running Tests

All unit and integration tests are located under the components folder.

    ```bash
    python -m unittest discover -s components -p "test_*.py"
    ```

## 📊 Features & Analysis
•	Data Collection: Fetches events from the Ticketmaster Discovery API using a keyword filter (concert by default).
•	Normalization: Supports city name aliases (e.g., nyc → New York, la → Los Angeles).
•	Data Persistence: Saves events to SQLite with duplicate protection.
•	Analysis: Events are sorted by date and limited to 20 for display.
•	Search: User can input a city; if empty, defaults to multiple Florida cities.