# app/storage/db.py
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Create DB file inside the project folder
DB_PATH = Path(__file__).resolve().parent / "memecoin_data.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            id TEXT PRIMARY KEY,
            name TEXT,
            liquidity REAL,
            holders INTEGER,
            lp_lock REAL,
            age_minutes INTEGER,
            score REAL,
            detected_at TEXT,
            data_json TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_token(token_id: str, name: str, liquidity: float,
                holders: int, lp_lock: float, age_minutes: int,
                score: float, data: dict):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO tokens (
            id, name, liquidity, holders, lp_lock, age_minutes, score, detected_at, data_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        token_id, name, liquidity, holders, lp_lock, age_minutes, score,
        datetime.utcnow().isoformat(), json.dumps(data)
    ))
    conn.commit()
    conn.close()

def get_latest_tokens(limit: int = 20):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tokens ORDER BY detected_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
