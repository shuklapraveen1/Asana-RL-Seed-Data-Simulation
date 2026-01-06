import sqlite3
import os


def init_db(db_path: str) -> sqlite3.Connection:
    """
    Initializes the SQLite database.
    - Creates database file if it does not exist
    - Enables foreign key constraints
    - Executes schema.sql to create tables
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)

    # Enable foreign key support
    conn.execute("PRAGMA foreign_keys = ON;")
    

    # Load schema.sql
    schema_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "schema.sql"
    )

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    # Execute schema
    conn.executescript(schema_sql)
    conn.commit()

    return conn
