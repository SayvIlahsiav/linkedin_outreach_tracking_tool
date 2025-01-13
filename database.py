import sqlite3

def connect_db():
    return sqlite3.connect("outreach.db")

def get_entries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM outreach")
    entries = cursor.fetchall()
    conn.close()
    return entries

def update_status(entry_id, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE outreach SET status = ? WHERE id = ?", (status, entry_id))
    conn.commit()
    conn.close()
