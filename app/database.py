# database.py
import sqlite3

def get_connection():
    conn = sqlite3.connect("library.db")
    conn.row_factory = sqlite3.Row  # supaya bisa akses kolom dengan nama
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabel Buku
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT,
        year INTEGER,
        borrowed_count INTEGER DEFAULT 0
    )
    """)

    # Tabel Anggota
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
    """)

    # Tabel Peminjaman
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        loan_date TEXT,
        return_date TEXT,
        returned INTEGER DEFAULT 0,
        fine REAL DEFAULT 0,
        FOREIGN KEY(book_id) REFERENCES books(id),
        FOREIGN KEY(member_id) REFERENCES members(id)
    )
    """)
    conn.commit()
    conn.close()
