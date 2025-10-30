import sqlite3
import datetime

DATABASE_NAME = "scraped_data.db"

def init_db():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # Create the table to store scraped content
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraped_content (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        content TEXT NOT NULL,
        scraped_at TIMESTAMP NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    print("Database initialized.")

def add_scraped_data(url: str, content: str):
    """Adds or replaces scraped data for a given URL."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now()
    # Use INSERT OR REPLACE to update the content if the URL already exists
    cursor.execute(
        """
        INSERT INTO scraped_content (url, content, scraped_at)
        VALUES (?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            content=excluded.content,
            scraped_at=excluded.scraped_at;
        """,
        (url, content, timestamp)
    )
    conn.commit()
    conn.close()

def get_content_by_url(url: str):
    """Retrieves the content for a specific URL."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM scraped_content WHERE url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_scraped_data():
    """Retrieves all stored records from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    # This makes the output a dictionary-like object, which is easier to work with
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, url, scraped_at FROM scraped_content ORDER BY scraped_at DESC")
    rows = cursor.fetchall()
    conn.close()
    # Convert the database rows to a list of dictionaries for JSON compatibility
    return [dict(row) for row in rows]