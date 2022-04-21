import sqlite3
import json
from models import Entry, Mood, Tag

def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./daily-journal.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date,
            m.label 
        FROM Entry e 
        JOIN Mood m
            ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                        row['date'])

            # Create a Mood instance from the current row
            mood = Mood(row['id'], row['label'])

            # Add the dictionary representation of the mood to the entry
            entry.mood = mood.__dict__

            # Before we get all entries we want to check for tags
            # so we can add them to the entries
            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM entry e
            JOIN entrytag et
                ON e.id = et.entry_id
            JOIN tag t
                ON t.id = et.tag_id
            WHERE e.id = ?
            """, (entry.id, ))

            # Fetch the tags
            tagList = db_cursor.fetchall()

            for row in tagList:
                tag = Tag(row['id'], row['name'])
                entry.tags.append(tag.__dict__)

            # Add tags to the entries
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./daily-journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM entry e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['mood_id'],
                    data['date'])

        return json.dumps(entry.__dict__)

def delete_entry(id):
    with sqlite3.connect("./daily-journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM entry
        WHERE id = ?
        """, (id, ))

def get_entries_by_search(string_variable):

    with sqlite3.connect("./daily-journal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            e.date
        FROM Entry e
        WHERE e.entry LIKE ?
        """, ( '%' + string_variable + '%', ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                        row['mood_id'], row['date'])
            entries.append(entry.__dict__)

    return json.dumps(entries)

def update_entry(id, new_entry):
    with sqlite3.connect("./daily-journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'],
            new_entry['date'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def create_entry(new_entry):
    with sqlite3.connect("./daily-journal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, mood_id, date )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'],
                new_entry['date'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the databse.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id

        # Loop through the tags after adding new entry
        # Inside the loop execute another SQL command
        # to add a row to the entrytag table.
        for tag in new_entry['tags']:

            db_cursor.execute("""
            INSERT INTO EntryTag
                (entry_id, tag_id)
            VALUES
                (?, ?);
            """, (id, tag))

    return json.dumps(new_entry)