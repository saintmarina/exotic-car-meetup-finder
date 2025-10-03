from flask import Flask, request, render_template_string
import sqlite3

# Reuse collector functions
from components.data_collector.src.main.collector import init_db, collect_for_city, DB_FILE
from components.data_analyzer.src.main.analyzer import get_sorted_events

app = Flask(__name__)

# Initialize DB once
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    city = None
    if request.method == "POST":
        city = request.form.get("city")
        if city:
            print(f"Fetching events for: {city}")
            collect_for_city(city)  # fetch + save to DB

    # If city provided, show only that city’s events
    if city:
        rows = get_sorted_events(DB_FILE, city=city)
    else:
        rows = get_sorted_events(DB_FILE)

    template = """
    <h1>Exotic Car & Concert Events in Florida</h1>
    <form method="POST">
      <input type="text" name="city" placeholder="Enter city name">
      <input type="submit" value="Search">
    </form>
    <p>Total events analyzed: {{ rows|length }}</p>
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