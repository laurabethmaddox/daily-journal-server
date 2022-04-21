import sqlite3
import json
from models import EntryTag

def get_all_entrytags():
    # Open a connection to the database
    with sqlite3.connect("./daily-journal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM entrytag et
        """)

        # Initialize an empty list to hold all mood representations
        entrytags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:
            entrytag = EntryTag(row['id'], row['entry_id'], row['tag_id'])
            entrytags.append(entrytag.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entrytags)