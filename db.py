import sqlite3

def init_db():
    conn = sqlite3.connect("tokens.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contract TEXT UNIQUE,
        name TEXT,
        symbol TEXT,
        status TEXT,
        volume REAL,
        liquidity REAL,
        dev TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn
