#Setting up Database
from pathlib import Path
from typing import List, Dict
import sqlite3

#Creation of Database in the homepage
DB_DIR = Path.home() / ".wlx"
DB_PATH = DB_DIR / "wlx.db"

def get_connection():
    """
    Creates and returns a database connection for WLX 
    """
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """ Initializing the database with rows & coloumns"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS wordlists (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       path TEXT UNIQUE,
                       size INTEGER,
                       mtime INTEGER,
                       tags TEXT
                   )
                   """)
    conn.commit()
    conn.close()


def upsert_wordlist(file_data: dict):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO wordlists (name, path, size, mtime, tags)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET
            name=excluded.name,
            size=excluded.size,
            mtime=excluded.mtime
    """, (
        file_data["name"],
        file_data["path"],
        file_data["size"],
        file_data["mtime"],
        file_data.get("tags", "")
    ))

    conn.commit()
    conn.close()
  
    
def search_wordlists(query: str, tags: list[str] = None):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM wordlists WHERE name LIKE ?"
    params = [f"%{query}%"]

    if tags:
        for tag in tags:
            sql += " AND tags LIKE ?"
            params.append(f"%{tag.lower()}%")

    sql += " ORDER BY name ASC"

    cursor.execute(sql, params)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def get_wordlist_by_id(wordlist_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM wordlists WHERE id = ?
    """, (wordlist_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)

    return None


def get_wordlist_count():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM wordlists")
    count = cursor.fetchone()[0]

    conn.close()
    return count


def add_tag(wordlist_id: int, tag: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Get current tags
    cursor.execute("SELECT tags FROM wordlists WHERE id = ?", (wordlist_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    current_tags = row["tags"] or ""

    # Convert to set (avoid duplicates)
    tag_set = set(t.strip() for t in current_tags.split(",") if t)

    tag = tag.lower().strip()
    tag_set.add(tag)

    updated_tags = ",".join(sorted(tag_set))

    # Update DB
    cursor.execute(
        "UPDATE wordlists SET tags = ? WHERE id = ?",
        (updated_tags, wordlist_id)
    )

    conn.commit()
    conn.close()

    return True


def remove_tag(wordlist_id: int, tag: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch current tags
    cursor.execute("SELECT tags FROM wordlists WHERE id = ?", (wordlist_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return False

    current_tags = row["tags"] or ""

    tag_set = set(t.strip() for t in current_tags.split(",") if t)

    tag = tag.lower().strip()

    if tag not in tag_set:
        conn.close()
        return "not_found"

    tag_set.remove(tag)

    updated_tags = ",".join(sorted(tag_set))

    cursor.execute(
        "UPDATE wordlists SET tags = ? WHERE id = ?",
        (updated_tags, wordlist_id)
    )

    conn.commit()
    conn.close()

    return True
    
    
    