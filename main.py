from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("outreach.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS outreach (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            profile_url TEXT,
            headline TEXT,
            personal_note TEXT,
            date_sent TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

# Add a new entry
def add_entry(profile_url, personal_note):
    conn = sqlite3.connect("outreach.db")
    cursor = conn.cursor()

    # Scrape name and headline from LinkedIn (simplified mock)
    try:
        response = requests.get(profile_url)
        soup = BeautifulSoup(response.content, "html.parser")
        name = soup.title.string  # Mock name
        headline = "Mock headline"  # Replace with actual scraping logic
    except Exception:
        name, headline = "Unknown", "Unknown"

    cursor.execute("""
        INSERT INTO outreach (name, profile_url, headline, personal_note, date_sent, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, profile_url, headline, personal_note, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Request Sent"))
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        profile_url = request.form["profile_url"]
        personal_note = request.form["personal_note"]
        add_entry(profile_url, personal_note)
        return "Entry added!"
    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
